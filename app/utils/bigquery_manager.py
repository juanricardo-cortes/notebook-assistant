from google.cloud import bigquery
from google.oauth2 import service_account # type: ignore
import uuid
import logging

class BigQueryManager:
    def __init__(self, project_id, dataset_id, credentials):
        """
        credentials: can be a path to a service account JSON file,
                     a credentials dictionary,
                     or a google.auth.credentials.Credentials object.
        """
        if isinstance(credentials, str):
            self.credentials = service_account.Credentials.from_service_account_file(credentials)
        elif isinstance(credentials, dict):
            self.credentials = service_account.Credentials.from_service_account_info(credentials)
        else:
            self.credentials = credentials

        self.client = bigquery.Client(project=project_id, credentials=self.credentials)
        self.dataset_id = f"{project_id}.{dataset_id}"
        self._initialize_dataset()
        self._initialize_tables()
        
    def _initialize_dataset(self):
        """Create BigQuery dataset if not exists"""
        dataset = bigquery.Dataset(self.dataset_id)
        dataset.location = "US"
        try:
            self.client.create_dataset(dataset, exists_ok=True)
            logging.info(f"Dataset {self.dataset_id} created or exists")
        except Exception as e:
            logging.error(f"Dataset creation failed: {str(e)}")
            raise

    def _initialize_tables(self):
        """Create required tables with partitioning and clustering"""
        tables = {
            "clients": [
                bigquery.SchemaField("client_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("email", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("signup_date", "DATE")
            ],
            "packages": [
                bigquery.SchemaField("package_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("tier_name", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("monthly_price", "FLOAT64"),
                bigquery.SchemaField("allocated_credits", "INT64")
            ],
            "subscriptions": [
                bigquery.SchemaField("subscription_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("client_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("package_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("start_date", "DATE"),
                bigquery.SchemaField("end_date", "DATE")
            ],
            "credit_balances": [
                bigquery.SchemaField("balance_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("subscription_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("allocated_credits", "INT64"),
                bigquery.SchemaField("used_credits", "INT64"),
                bigquery.SchemaField("reset_date", "DATE")
            ]
        }

        for table_name, schema in tables.items():
            table_ref = f"{self.dataset_id}.{table_name}"
            table = bigquery.Table(table_ref, schema=schema)
            
            # Add partitioning for credit_balances
            if table_name == "credit_balances":
                table.time_partitioning = bigquery.TimePartitioning(
                    type_=bigquery.TimePartitioningType.MONTH,
                    field="reset_date"
                )
                table.clustering_fields = ["subscription_id"]

            try:
                self.client.create_table(table, exists_ok=True)
                logging.info(f"Table {table_name} created or exists")
            except Exception as e:
                logging.error(f"Table creation failed for {table_name}: {str(e)}")
                raise

        # Initialize package tiers if not exists
        self._seed_initial_packages()

    def _seed_initial_packages(self):
        """Insert initial package tiers if the table is empty"""
        packages = [
            {"package_id": "basic", "tier_name": "Basic", "monthly_price": 29.00, "allocated_credits": 300},
            {"package_id": "pro", "tier_name": "Pro", "monthly_price": 99.00, "allocated_credits": 1000},
            {"package_id": "enterprise", "tier_name": "Enterprise", "monthly_price": 299.00, "allocated_credits": None}
        ]

        # Check if the table is empty
        query_check = f"SELECT COUNT(*) AS count FROM `{self.dataset_id}.packages`"
        result = self.client.query(query_check).result()
        row = list(result)[0]
        if row.count > 0:
            logging.info("Packages table already has data. Skipping seed.")
            return

        # Insert initial packages
        query_insert = f"""
            INSERT INTO `{self.dataset_id}.packages` (package_id, tier_name, monthly_price, allocated_credits)
            VALUES (@package_id, @tier_name, @monthly_price, @allocated_credits)
        """

        for package in packages:
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("package_id", "STRING", package["package_id"]),
                    bigquery.ScalarQueryParameter("tier_name", "STRING", package["tier_name"]),
                    bigquery.ScalarQueryParameter("monthly_price", "FLOAT64", package["monthly_price"]),
                    bigquery.ScalarQueryParameter("allocated_credits", "INT64", package["allocated_credits"]),
                ]
            )
            self.client.query(query_insert, job_config=job_config).result()

        logging.info("Initial packages inserted successfully.")

    def create_client(self, email):
        """Create a new client in BigQuery"""
        client_id = str(uuid.uuid4())
        query = f"""
            INSERT `{self.dataset_id}.clients` (client_id, email, signup_date)
            VALUES (@client_id, @email, CURRENT_DATE())
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("client_id", "STRING", client_id),
                bigquery.ScalarQueryParameter("email", "STRING", email)
            ]
        )
        self.client.query(query, job_config=job_config).result()
        return client_id

    def create_subscription(self, client_id, package_id):
        """Create a new subscription in BigQuery"""
        sub_id = str(uuid.uuid4())
        query = f"""
            INSERT `{self.dataset_id}.subscriptions` 
            (subscription_id, client_id, package_id, start_date)
            VALUES (
                @sub_id,
                @client_id,
                @package_id,
                CURRENT_DATE()
            )
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("sub_id", "STRING", sub_id),
                bigquery.ScalarQueryParameter("client_id", "STRING", client_id),
                bigquery.ScalarQueryParameter("package_id", "STRING", package_id)
            ]
        )
        self.client.query(query, job_config=job_config).result()
        return sub_id

    def initialize_credits(self, subscription_id):
        """Initialize credit balance for a subscription"""
        query = f"""
            INSERT `{self.dataset_id}.credit_balances` 
            (balance_id, subscription_id, allocated_credits, used_credits, reset_date)
            SELECT 
                GENERATE_UUID(),
                @subscription_id,
                p.allocated_credits,
                0,
                DATE_TRUNC(CURRENT_DATE(), MONTH)
            FROM `{self.dataset_id}.subscriptions` s
            JOIN `{self.dataset_id}.packages` p 
                USING(package_id)
            WHERE subscription_id = @subscription_id
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("subscription_id", "STRING", subscription_id)
            ]
        )
        self.client.query(query, job_config=job_config).result()

    def subtract_credits(self, subscription_id, credits):
        """Subtract credits with monthly reset handling"""
        query = f"""
            UPDATE `{self.dataset_id}.credit_balances`
            SET used_credits = used_credits + @credits
            WHERE subscription_id = @subscription_id
              AND reset_date = DATE_TRUNC(CURRENT_DATE(), MONTH)
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("subscription_id", "STRING", subscription_id),
                bigquery.ScalarQueryParameter("credits", "INT64", credits)
            ]
        )
        self.client.query(query, job_config=job_config).result()

