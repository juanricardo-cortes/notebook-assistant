import sys
import json
import os
import time
import concurrent.futures

from scrapers.youtube_service import YouTubeService
from scrapers.twitter_service import TwitterScraper
from scrapers.instagram_service import InstagramScraper
from scrapers.linkedin_service import LinkedInScraper
from scrapers.facebook_service import FacebookService
from scrapers.newsletter_service import NewsletterService
from scrapers.perplexity_service import PerplexityService
from scrapers.gemini_service import GeminiService

from monitors.social_monitor import SocialMonitor

from core.driver import AntiDetectDriver
from core.proxy_manager import FreeProxyManager
from core.rate_limiter import RateLimiter

from utils.drive_manager import GoogleDriveUploader
from utils.gmail_manager import GmailService
from utils.credentials_provider import CredentialsProvider
from utils.email_provider import EmailProvider
from utils.openai_manager import OpenAIService
from utils.bigquery_manager import BigQueryManager

from features.notebook_default import NotebookDefault


# Load configuration from the config file
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config", "config.json")
with open(CONFIG_PATH, "r") as config_file:
    CONFIG = json.load(config_file)

def main(args=None):
    if args is None:
        args = []
    else: 
        # Log the received arguments
        print(f"Received arguments: {args}")

        # start_proxy_rotation()        
        # start_email_provider()

        # test()
        start_monitoring()
        # start_bigquery()
    
    return

def start_monitoring():
    print("Starting monitoring...")
    #1 new_ai_tools
    #2 new_ai_updates_and_improvements
    #3 new_ai_business_innovations_and_applications
    #4 new_ai_discussions_and_trends

    def run_monitor(func):
        try:
            return func()
        except Exception as e:
            print(f"Error in {func.__name__}: {e}")
            return tuple([] for _ in range(12))  # 4 categories x (data, links, titles)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_linkedin = executor.submit(run_monitor, monitor_linkedin_profiles)
        future_instagram = executor.submit(run_monitor, monitor_instagram_profiles)
        future_newsletter = executor.submit(run_monitor, monitor_newsletters)
        future_youtube = executor.submit(run_monitor, monitor_youtube_channels)
        future_twitter = executor.submit(run_monitor, monitor_twitter_profiles)
        future_facebook = executor.submit(run_monitor, monitor_facebook_groups)
        future_perplexity = executor.submit(run_monitor, monitor_perplexity_prompts)
        future_gemini = executor.submit(run_monitor, monitor_gemini_prompts)

        (linkedin_data1, linkedin_data2, linkedin_data3, linkedin_data4,
         linkedin_summary1, linkedin_summary2, linkedin_summary3, linkedin_summary4) = future_linkedin.result()

        (instagram_data1, instagram_data2, instagram_data3, instagram_data4,
         instagram_summary1, instagram_summary2, instagram_summary3, instagram_summary4) = future_instagram.result()

        (newsletter_data1, newsletter_data2, newsletter_data3, newsletter_data4,
         newsletter_summary1, newsletter_summary2, newsletter_summary3, newsletter_summary4) = future_newsletter.result()

        (youtube_data1, youtube_data2, youtube_data3, youtube_data4,
         youtube_summary1, youtube_summary2, youtube_summary3, youtube_summary4) = future_youtube.result()

        (twitter_data1, twitter_data2, twitter_data3, twitter_data4,
         twitter_summary1, twitter_summary2, twitter_summary3, twitter_summary4) = future_twitter.result()

        (facebook_data1, facebook_data2, facebook_data3, facebook_data4,
         facebook_summary1, facebook_summary2, facebook_summary3, facebook_summary4) = future_facebook.result()
        
        (perplexity_data1, perplexity_data2, perplexity_data3, perplexity_data4,
         perplexity_summary1, perplexity_summary2, perplexity_summary3, perplexity_summary4) = future_perplexity.result()
        
        (gemini_data1, gemini_data2, gemini_data3, gemini_data4,
         gemini_summary1, gemini_summary2, gemini_summary3, gemini_summary4) = future_gemini.result()
        
    print("FINISHED MONITORING")
    # Initialize lists for each category
    all_files1, all_files2, all_files3, all_files4 = [], [], [], []
    all_summaries1, all_summaries2, all_summaries3, all_summaries4 = [], [], [], []

    # Extend data for each category
    all_files1.extend(linkedin_data1); all_files2.extend(linkedin_data2); all_files3.extend(linkedin_data3); all_files4.extend(linkedin_data4)
    all_files1.extend(instagram_data1); all_files2.extend(instagram_data2); all_files3.extend(instagram_data3); all_files4.extend(instagram_data4)
    all_files1.extend(newsletter_data1); all_files2.extend(newsletter_data2); all_files3.extend(newsletter_data3); all_files4.extend(newsletter_data4)
    all_files1.extend(youtube_data1); all_files2.extend(youtube_data2); all_files3.extend(youtube_data3); all_files4.extend(youtube_data4)
    all_files1.extend(twitter_data1); all_files2.extend(twitter_data2); all_files3.extend(twitter_data3); all_files4.extend(twitter_data4)
    all_files1.extend(facebook_data1); all_files2.extend(facebook_data2); all_files3.extend(facebook_data3); all_files4.extend(facebook_data4)
    all_files1.extend(perplexity_data1); all_files2.extend(perplexity_data2); all_files3.extend(perplexity_data3); all_files4.extend(perplexity_data4)
    all_files1.extend(gemini_data1); all_files2.extend(gemini_data2); all_files3.extend(gemini_data3); all_files4.extend(gemini_data4)

    # Extend summaries for each category
    all_summaries1.extend(linkedin_summary1); all_summaries2.extend(linkedin_summary2); all_summaries3.extend(linkedin_summary3); all_summaries4.extend(linkedin_summary4)
    all_summaries1.extend(instagram_summary1); all_summaries2.extend(instagram_summary2); all_summaries3.extend(instagram_summary3); all_summaries4.extend(instagram_summary4)
    all_summaries1.extend(newsletter_summary1); all_summaries2.extend(newsletter_summary2); all_summaries3.extend(newsletter_summary3); all_summaries4.extend(newsletter_summary4)
    all_summaries1.extend(youtube_summary1); all_summaries2.extend(youtube_summary2); all_summaries3.extend(youtube_summary3); all_summaries4.extend(youtube_summary4)
    all_summaries1.extend(twitter_summary1); all_summaries2.extend(twitter_summary2); all_summaries3.extend(twitter_summary3); all_summaries4.extend(twitter_summary4)
    all_summaries1.extend(facebook_summary1); all_summaries2.extend(facebook_summary2); all_summaries3.extend(facebook_summary3); all_summaries4.extend(facebook_summary4)
    all_summaries1.extend(perplexity_summary1); all_summaries2.extend(perplexity_summary2); all_summaries3.extend(perplexity_summary3); all_summaries4.extend(perplexity_summary4)
    all_summaries1.extend(gemini_summary1); all_summaries2.extend(gemini_summary2); all_summaries3.extend(gemini_summary3); all_summaries4.extend(gemini_summary4)
        
    # Process and upload for all_files1
    if not all_files1:
        print("No data to process for category 1. Stopping execution.")
    else:
        if start_notebook_assistant(all_files1):
            print("Monitoring for category 1 completed.")
            start_google_drive(all_summaries1, subject="NEW TOOLS")
            print("Google Drive upload for category 1 completed.")

    # Process and upload for all_files2
    if not all_files2:
        print("No data to process for category 2. Stopping execution.")
    else:
        if start_notebook_assistant(all_files2):
            print("Monitoring for category 2 completed.")
            start_google_drive(all_summaries2, subject="UPDATES AND IMPROVEMENTS")
            print("Google Drive upload for category 2 completed.")

    # Process and upload for all_files3
    if not all_files3:
        print("No data to process for category 3. Stopping execution.")
    else:
        if start_notebook_assistant(all_files3):
            print("Monitoring for category 3 completed.")
            start_google_drive(all_summaries3, subject="BUSINESS INNOVATIONS")
            print("Google Drive upload for category 3 completed.")

    # Process and upload for all_files4
    if not all_files4:
        print("No data to process for category 4. Stopping execution.")
    else:
        if start_notebook_assistant(all_files4):
            print("Monitoring for category 4 completed.")
            start_google_drive(all_summaries4, subject="DISCUSSIONS")
            print("Google Drive upload for category 4 completed.")
    print("COMPLETED")

def monitor_newsletters():
    newsletter_scraper = NewsletterService(config=CONFIG)
    newsletter_urls = CONFIG["newsletter_urls"]
    monitor = SocialMonitor(newsletter_scraper, newsletter_urls, CONFIG)
    processed_data = monitor.execute_monitoring()
    return processed_data

def monitor_youtube_channels():
    api_key = CONFIG["youtube_api_key"]
    channel_urls = CONFIG["youtube_channels"]
    youtube_service = YouTubeService(api_key)
    monitor = SocialMonitor(youtube_service, channel_urls, CONFIG)
    processed_data = monitor.execute_monitoring()
    return processed_data

def monitor_twitter_profiles():
    driver = AntiDetectDriver().get_driver()
    twitter_scraper = TwitterScraper(driver)
    twitter_profiles = CONFIG["twitter_profiles"]
    monitor = SocialMonitor(twitter_scraper, twitter_profiles, CONFIG)
    processed_data = monitor.execute_monitoring()
    return processed_data

def monitor_instagram_profiles():
    instagram_scraper = InstagramScraper(config=CONFIG)
    instagram_profiles = CONFIG["instagram_profiles"]
    monitor = SocialMonitor(instagram_scraper, instagram_profiles, CONFIG)
    processed_data = monitor.execute_monitoring()
    return processed_data

def monitor_linkedin_profiles():
    linkedin_scraper = LinkedInScraper(config=CONFIG)
    linkedin_profiles = CONFIG["linkedin_profiles"]
    monitor = SocialMonitor(linkedin_scraper, linkedin_profiles, CONFIG)
    processed_data = monitor.execute_monitoring()
    return processed_data

def monitor_facebook_groups():
    facebook_scraper = FacebookService(config=CONFIG)
    facebook_groups = CONFIG["facebook_groups"]
    monitor = SocialMonitor(facebook_scraper, facebook_groups, CONFIG)
    processed_data = monitor.execute_monitoring()
    return processed_data

def monitor_perplexity_prompts():
    perplexity_scraper = PerplexityService(config=CONFIG)
    perplexity_prompts = ai_scrape_prompts
    monitor = SocialMonitor(perplexity_scraper, perplexity_prompts, CONFIG)
    processed_data = monitor.execute_monitoring()
    return processed_data

def monitor_gemini_prompts():
    gemini_scraper = GeminiService(config=CONFIG)

    gemini_prompts = ai_scrape_prompts
    monitor = SocialMonitor(gemini_scraper, gemini_prompts, CONFIG)
    processed_data = monitor.execute_monitoring()
    return processed_data

def start_proxy_rotation():
    proxy_manager = FreeProxyManager()
    all_proxies = proxy_manager.get_proxy_list()
    print(f"Found {len(all_proxies)} proxies")
    working_proxy = proxy_manager.get_random_proxy()
    print(f"Random working proxy: {working_proxy}")

def start_email_provider():
    mail_api = EmailProvider()
    for _ in range(3):
        email, password = mail_api.create_email_with_credentials()
        print("Generated Email:", email)
        print("Generated Password:", password)
        RateLimiter.random_delay()

def start_notebook_assistant(processed_data):
    driver = AntiDetectDriver().get_driver()
    notebook_assistant = NotebookDefault(driver=driver)
    return notebook_assistant.generate_audio_podcast_from_profiles(processed_data)

def start_google_drive(all_summaries, subject):
    time.sleep(10)  # Wait for the file to be ready
    
    summaries_text = "\n".join(all_summaries)
    openai_service = OpenAIService(config=CONFIG)
    instructions = CONFIG["title_prompt"]
    prompt = f"{instructions}: Content: {summaries_text}"
    response = openai_service.generate_response(prompt, instructions)

    credentials_provider = CredentialsProvider(CONFIG)
    credentials = credentials_provider.get_credentials(CONFIG["drive_email"])
    uploader = GoogleDriveUploader(credentials=credentials)
    uploader.authenticate()
    file_metadata = uploader.upload_file(title=response, emails_to_share=CONFIG["emails_to_share"])

    openai_service = OpenAIService(config=CONFIG)
    instructions = CONFIG["summarize_prompt"]
    prompt = f"{instructions}: Content: {summaries_text}"
    response = openai_service.generate_response(prompt, instructions)

    body_with_links = f"{subject}: Daily podcast update has been uploaded to Google Drive. Link: {file_metadata['webViewLink']}\n\nAdditional Links:\n{response}"
    for email in CONFIG["emails_to_share"]:
        gmail_service = GmailService(credentials=credentials)
        gmail_service.send_email(
            to=email,
            subject=f'[{subject}]: Daily Ai Podcast Updates',
            body=body_with_links
        )

def start_bigquery():
    credentials_provider = CredentialsProvider(CONFIG)
    credentials = credentials_provider.get_credentials(CONFIG["bigquery_email"])
    project_id = CONFIG["project_id"]
    dataset_id = CONFIG["dataset_id"]
    
    bigquery_manager = BigQueryManager(project_id, dataset_id, credentials)
    print(f"BigQuery dataset {dataset_id} initialized successfully.")

def test():
    print("Testing...")

ai_scrape_prompts = ["""
DEEP RESEARCH

**Prompt for Gemini 2.5 Pro Deep Research: Uncovering Novel AI Tool Releases**

**Role:** You are an AI Research Scout specializing in identifying and detailing newly launched, lesser-known AI tools, platforms, models, and significant open-source projects. Your expertise lies in sifting through non-mainstream channels to find nascent innovations.

**Primary Objective:**
Identify and report on AI tools, software, platforms, models, APIs, libraries, or significant open-source projects that have been publicly announced, released, or had their first significant public mention *for the first time* within the **last 24 hours** from the exact time of this query.

**Definition of 'New Tool' for this Task:**
*   **In-Scope:**
    *   Completely new AI-powered applications, software, or services.
    *   Newly released open-source AI models or significant code repositories (e.g., on GitHub, Hugging Face).
    *   New AI platforms or APIs available for developers or public use.
    *   Bootstrap projects, tools from indie developers, startups, or research labs that are not yet widely known.
    *   Initial 'v0.1' or 'v1.0' releases, public beta launches, or 'Show HN' style announcements.
*   **Out-of-Scope (Crucial Exclusions):**
    *   Updates, new features, or new versions of *existing, well-established, and widely known* AI tools (e.g., do NOT report an update to Google Gemini, OpenAI ChatGPT, Midjourney, Claude, Microsoft Copilot, etc., unless it is a *fundamentally new, standalone product* launched by these companies).
    *   General AI news articles, opinion pieces, or trend discussions.
    *   Announcements of funding rounds for existing companies unless tied directly to an immediate new tool release.
    *   Research papers *unless* they are accompanied by a concurrently released, usable tool, codebase, or live demo.
    *   Minor bug fixes or incremental library updates.

**Prioritized Information Sources (Leverage Deep Research Capabilities to scan):**
Focus your search primarily on, but not limited to:
1.  **Reddit:**
    *   Subreddits: r/ArtificialIntelligence, r/MachineLearning, r/LocalLLaMA, r/Singularity, r/AItools, r/SideProject, r/Programming, r/OpenSource, r/HuggingFace, r/StableDiffusion, r/ControlNet, and niche AI subreddits.
    *   Look for: 'New tool,' 'I built,' 'Released,' 'Launched,' 'Showoff,' 'Open Source AI,' project announcements.
2.  **GitHub:**
    *   Search for: New repositories with tags like 'AI', 'machine-learning', 'deep-learning', 'LLM', 'generative-ai', 'neural-network', 'computer-vision', 'nlp'.
    *   Filter by: Recently updated or created, initial commits, release tags (v0.1, v1.0).
    *   Scan: README files for release announcements or project goals.
3.  **Hugging Face:**
    *   Sections: New Models, new Datasets, new Spaces.
    *   Look for: Contributions from individual developers, smaller research groups, or new organizations.
4.  **X (formerly Twitter):**
    *   Search for: Hashtags like #AI, #NewAI, #AITool, #GenerativeAI, #LLM, #OpenSourceAI, #AIlaunch, #IndieDev, #BuildInPublic.
    *   Monitor: Feeds of AI researchers, developers, startup founders, and AI community influencers known for sharing new/niche tools.
5.  **Specialized AI Newsletters & Blogs:**
    *   Focus on: Niche publications, community blogs, and newsletters that cover early-stage or indie AI developments (e.g., those that syndicate content from places like Product Hunt, Indie Hackers).
6.  **Product Hunt:** Check for new AI-related product launches.
7.  **Indie Hackers & Hacker News (Y Combinator):**
    *   Look for: 'Show HN' posts, discussions about new AI projects, or self-promotions of new tools.
8.  **Relevant Discord Servers & Online Communities:** If accessible, scan channels dedicated to new AI tools or project showcases.

**Information to Extract for Each Identified Tool/Project (Mandatory Fields):**
For *each* new tool/project identified, provide the following details:

1.  **Tool Name:**
2.  **Date & Time of Release/First Public Announcement:** (Must be within the last 24 hours. Specify the source of this date).
3.  **Source(s) of Discovery:** (Direct URL(s) to the announcement, GitHub repo, website, social media post, etc. Prioritize primary sources).
4.  **One-Sentence Summary:** (What is it / what does it do?)
5.  **Core Problem It Solves / Primary Use Case(s):**
6.  **Key Features/Capabilities:** (List 2-4 bullet points).
7.  **Technology Stack/Underlying Model (if discernible):** (e.g., 'Python library,' 'Uses Llama 3,' 'Web app built with React,' 'Finetuned Stable Diffusion model').
8.  **Developer/Company Information:**
    *   **Name:** (Company name, individual developer's handle/name, or research lab).
    *   **Brief Background:** (e.g., 'Indie developer,' 'New startup,' 'University research project.' If a company, a very brief note on its focus if readily available. Is this their first product?).
9.  **Target Audience:** (e.g., Developers, researchers, marketers, artists, general public).
10. **Access/Pricing Model:** (e.g., Open Source (specify license if possible), Freemium, Paid, Free Beta, API with pricing tiers, Waitlist).
11. **Perceived Novelty/Innovation Factor:** (Briefly explain why this tool is interesting or different, especially in the context of being a *new*, potentially lesser-known release. Is it a novel application, a new open model, a useful utility for a niche AI task?).
12. **Category Suggestion:** (e.g., Text Generation, Image Generation, Audio Synthesis, Code Assistant, Data Analysis, AI Ethics Tool, Developer Tool, Research Tool, Productivity AI, etc.)

**Output Format & Organization:**
*   Present findings as a list of distinct tools.
*   For each tool, use the exact field names listed above in a clear, structured format (e.g., using markdown headings or bolded labels for each field).
*   If no tools matching the strict criteria are found within the last 24 hours, explicitly state 'No new AI tools matching the specified criteria were identified within the last 24 hours from the prioritized sources.'
*   Order the tools chronologically by release time if possible, otherwise by your discovery order.

**Search Strategy Guidance:**
*   Prioritize direct announcements over secondary reporting.
*   Use advanced search operators on platforms like Google, X, and GitHub (e.g., `site:github.com 'new AI tool' created:>YYYY-MM-DDTHH:MM:SSZ`, time-filtered searches on X).
*   Be wary of marketing language; focus on actual releases and functionality.
*   Cross-reference information if possible to confirm newness and details.

**Final Check:** Before reporting a tool, perform a quick mental check: 'Is this something likely to be missed by major tech news outlets today? Is it genuinely *new* (not an update)? Does it come from a smaller entity or an individual?' If yes to these, it's likely a good candidate.

---

**Why this prompt is designed this way for Gemini 2.5 Pro Deep Research:**

*   **Specificity:** Leaves little room for ambiguity, which is key for LLMs.
*   **Deep Research Cues:** Phrases like 'Leverage Deep Research Capabilities,' 'sifting through non-mainstream channels,' and listing specific, sometimes obscure, sources tell Gemini to go beyond standard search engine results.
*   **Exclusion Focus:** Repeatedly emphasizing what *not* to include is as important as what to include, especially for avoiding common news.
*   **Structured Output:** Makes the information immediately usable for your podcast database. The fields are designed for quick assessment.
*   **Developer/Company Focus:** Your request to know 'a little bit about the company' is directly addressed.
*   **Innovation Angle:** The 'Perceived Novelty/Innovation Factor' field encourages Gemini to think about *why* this tool is interesting beyond just existing.
*   **Categorization:** Helps you organize the findings for your podcast segments.

This prompt is quite long, but for a complex task requiring deep, targeted research, detail is your friend. You want to give Gemini as much context and constraint as possible to get the high-quality, specific results you're looking for. Remember to replace `YYYY-MM-DDTHH:MM:SSZ` with the actual timestamp from 24 hours prior to your query if you're trying to manually construct such a search, though Gemini should handle the 'last 24 hours' instruction well.
/llm/prompt/newaitools
""",
"""
DEEP RESEARCH
**Prompt for Gemini 2.5 Pro Deep Research: Analyzing Significant AI Tool Updates & Ecosystem Impact**

**Role:** You are an AI Technology Analyst and Ecosystem Commentator. Your expertise lies in identifying, detailing, and analyzing significant updates, improvements, and new capability releases for established, widely-used AI tools, platforms, agent ecosystems, and critical AI infrastructure. You focus on understanding the broader implications of these advancements.

**Primary Objective:**
Identify, report on, and analyze significant updates, new feature rollouts, version releases, or substantial improvements to *well-known and established* AI tools, software, platforms, models, APIs, or infrastructure components that have been publicly announced or released, primarily within the **last 7 days** (with flexibility for highly impactful announcements slightly older if still reverberating). The core focus is not just *what* the update is, but *why it matters* for the AI field and its users.

**Definition of 'Significant Update/Improvement' for this Task:**
*   **In-Scope:**
    *   Major new versions or models released for flagship AI products (e.g., a new iteration of Google Gemini, OpenAI's GPT series, Anthropic's Claude, Meta's Llama, Stability AI's models).
    *   Significant new features or capabilities added to these established tools (e.g., expanded context windows, new modalities, function calling enhancements, advanced reasoning abilities, significant performance breakthroughs).
    *   Important updates to popular AI agent frameworks or ecosystems (e.g., LangChain, AutoGen, CrewAI) that notably expand their capabilities or ease of use.
    *   New, impactful integrations between major AI tools or platforms that unlock novel workflows or significantly enhance existing ones.
    *   Releases of influential open-source models by major labs or consortiums that are expected to have a broad impact.
    *   Key advancements in AI infrastructure (e.g., new chip announcements with direct AI performance implications, significant updates to AI development platforms like Hugging Face Hub, NVIDIA AI Enterprise).
*   **Out-of-Scope (Crucial Exclusions):**
    *   Minor bug fixes, incremental performance tweaks without new feature announcements, or routine maintenance updates.
    *   UI/UX changes that don't fundamentally alter capabilities.
    *   Re-announcements or marketing repackaging of existing features.
    *   Purely theoretical research papers without an accompanying product/tool update or clear, immediate path to implementation in an existing tool.
    *   Launch of entirely new, *previously unknown* tools (this is covered by a separate research focus). We are interested in *updates to existing, known entities*.
    *   General AI news, opinion pieces, or funding announcements unless directly tied to a specific, significant product update detailed above.

**Prioritized Information Sources (Leverage Deep Research Capabilities to scan and synthesize):**
Focus your search and analysis primarily on, but not limited to:
1.  **Official Company Blogs & Announcements:** (OpenAI, Google DeepMind/AI, Meta AI, Anthropic, Microsoft AI, NVIDIA, Stability AI, Hugging Face, etc.)
2.  **Major Tech News Publications (AI Sections):** (e.g., The Verge, TechCrunch, Wired, MIT Technology Review, ZDNet, Ars Technica).
3.  **Leading AI-focused Newsletters & Publications:** (e.g., Ben's Bites, The Neuron, Import AI, LastWeekin.AI, and other reputable sources known for insightful AI news).
4.  **X (formerly Twitter):** Monitor feeds of official company accounts, prominent AI researchers, CEOs/CTOs of major AI labs, and respected AI commentators who often break or analyze such news.
5.  **Developer Forums & Communities:** (e.g., official forums for major AI tools, relevant GitHub discussions on major open-source projects).
6.  **Key Industry Analyst Reports/Briefings (if accessible via public search):** Sometimes analysts summarize the impact of major releases.

**Information to Extract for Each Identified Update/Improvement (Mandatory Fields):**
For *each* significant update/improvement identified, provide the following details:

1.  **Tool/Platform/Model Name:** (The established entity that received the update).
2.  **Update/Feature Name & Version (if applicable):** (e.g., 'Gemini 1.5 Pro - 1M Context Window Expansion,' 'GPT-4V API General Availability,' 'LangChain v0.X.Y - New Agent Executor').
3.  **Date of Announcement/Release:** (Must be primarily within the last 7 days, or slightly older if highly impactful and still being discussed).
4.  **Source(s) of Information:** (Direct URL(s) to official announcement, key news coverage, technical blog posts. Prioritize official sources).
5.  **Concise Summary of the Update:** (What specific changes, additions, or improvements were made?)
6.  **Key New Capabilities Unlocked or Existing Capabilities Significantly Enhanced:** (What can users/developers do now that they couldn't do as effectively or at all before this update? Be specific.)
7.  **Newly Enabled or Significantly Improved Integrations (if applicable):** (Does this update allow the tool to work better with other tools, platforms, or data sources?)
8.  **Target Audience Benefiting Most:** (e.g., Developers, researchers, enterprise users, specific industries, general consumers).
9.  **Potential Implications for the Broader AI Ecosystem:**
    *   How might this shift the competitive landscape among AI providers?
    *   Does it accelerate or enable new research directions?
    *   How does it impact accessibility or democratization of AI capabilities?
    *   Does it address any existing limitations or challenges in the AI field?
10. **Potential Impact on the AI Developer/User Community:**
    *   Does it lower the barrier to entry for certain AI applications?
    *   Does it enable new types of applications or use cases to be built more easily?
    *   How might it change workflows for developers or users of this tool?
11. **Why this Update is Considered Significant:** (Synthesize its importance. Is it a breakthrough, a major step forward, a competitive response, a foundational improvement for future developments?)
12. **Underlying Technological Advancements (if detailed in sources):** (e.g., 'New model architecture,' 'Improved training data/techniques,' 'Hardware optimization').

**Output Format & Organization:**
*   Present findings as a list of distinct updates/improvements.
*   For each item, use the exact field names listed above in a clear, structured format (e.g., using markdown headings or bolded labels for each field).
*   If no *significant* updates matching the criteria are found within the primary timeframe, explicitly state 'No major AI tool/platform updates matching the specified significance criteria were identified within the primary timeframe from the prioritized sources.'
*   Order the updates by perceived impact or by announcement date (most recent first).

**Search Strategy & Analytical Guidance:**
*   Focus on official announcements and reputable, analytical tech journalism over speculative posts.
*   Analyze *why* an update is being highlighted by the company or by commentators – what problem does it solve, or what new opportunity does it create?
*   Look for comparative language: 'faster than before,' 'more capable than X,' 'first to offer Y.'
*   Synthesize information from multiple sources if possible to get a well-rounded view of the update and its impact.

**Final Check:** Before reporting an update, ask: 'Is this a genuine step-change or a truly notable enhancement for a well-known AI entity, or just routine news? What are its likely ripple effects?'

---

**Key Differences & Focus for this Prompt:**

*   **Target:** Shifts from obscure/new to established/well-known.
*   **Nature of Information:** Focuses on *updates and improvements* to existing things, not brand-new entities.
*   **Analytical Depth:** Greatly emphasizes the 'implications' and 'impact' on the broader ecosystem and community. This requires more synthesis and understanding than just reporting a new tool.
*   **Timescale:** 'Last 7 days' is more appropriate for impactful updates to major tools, as these often have a news cycle that lasts a bit longer and their significance isn't always immediately apparent in the first 24 hours.
*   **Sources:** Leans more towards official channels of major players and reputable tech journalism that analyzes these players.

This prompt should guide Gemini 2.5 Pro Deep Research to provide the analytical and context-rich information you need for your podcast segment on major AI advancements.
/llm/prompt/aiupdates
""",
"""
DEEP RESEARCH
**Prompt for Gemini 2.5 Pro Deep Research: AI-Driven Business Innovation, Use Cases & Monetization for SMB-Focused Agent Solutions**

**Role:** You are an AI Business Innovation Analyst and Solutions Consultant, specializing in identifying and evaluating practical, monetizable AI applications for Small to Medium-Sized Businesses (SMBs). Your focus is on how recent AI advancements can be translated into tangible business value, particularly through managed AI agent solutions.

**Primary Objective:**
Identify, analyze, and report on novel and impactful ways businesses (with a strong emphasis on applications relevant or adaptable to SMBs) are currently applying recent AI innovations. For each identified use case, detail its business value, potential monetization strategies, and specific relevance for an AI agent building company that provides managed agent services to SMBs. Consider AI technologies and updates announced or gaining traction in roughly the **last 3-6 months**.

**Definition of 'Business Innovation & New Use Cases' for this Task:**
*   **In-Scope:**
    *   Specific, real-world examples or well-documented conceptual applications of how businesses are using AI to:
        *   Solve existing business problems more effectively.
        *   Create new revenue streams or service offerings.
        *   Significantly improve operational efficiency (e.g., automation of workflows, cost reduction).
        *   Enhance customer experience, sales, or marketing.
        *   Gain a competitive advantage.
    *   Applications leveraging recent AI advancements (e.g., more capable LLMs, multimodal AI, improved agentic frameworks, accessible fine-tuning, new AI-powered analytics).
    *   Use cases that are particularly well-suited for, or could be adapted to, delivery via AI agents (e.g., automated customer support, intelligent data entry & processing, proactive sales outreach, personalized marketing content generation, specialized research assistants).
    *   Examples from various industries that could inspire similar applications in other SMB sectors.
    *   Early-stage adoptions or innovative pilot projects by businesses demonstrating clear potential.
*   **Out-of-Scope (Crucial Exclusions):**
    *   Purely theoretical AI capabilities without clear business application pathways.
    *   General discussions about 'AI in X industry' without specific use case examples.
    *   Overly broad or generic AI benefits (e.g., 'AI improves efficiency' – need specifics).
    *   Complex, multi-million dollar enterprise-only solutions that have no clear adaptation path for SMBs or agent-based delivery.
    *   News about AI company funding or M&A *unless* it directly details a novel customer application or use case being deployed.
    *   Updates to AI tools themselves *unless* the focus is on *how businesses are now using those updated features* for new applications.

**Target Audience Focus for Insights:**
The primary beneficiary of this research is an **AI agent building company that provides managed AI agent services to Small to Medium-Sized Businesses (SMBs)**. Therefore, all findings should be analyzed through the lens of:
*   How can this use case be packaged and offered as a managed AI agent service?
*   What type of AI agent(s) would be required?
*   What value proposition does this offer to an SMB client?
*   What are the monetization opportunities for the agent building company?

**Prioritized Information Sources (Leverage Deep Research Capabilities to scan and synthesize):**
1.  **Business & Industry Publications:** (e.g., Forbes, Harvard Business Review (HBR) Ascend, Inc. Magazine, Entrepreneur, industry-specific trade journals and websites that discuss technology adoption).
2.  **Case Studies & White Papers:** From AI solution providers (even larger ones, if the core application can be scaled down or adapted), consultancies, and businesses themselves showcasing AI implementation successes.
3.  **Startup & Tech Blogs/Newsletters:** Focusing on B2B solutions, AI applications in business, and SaaS innovations.
4.  **LinkedIn Articles & Posts:** From business leaders, consultants, and AI practitioners sharing insights on AI adoption and use cases.
5.  **Product Hunt & Similar Platforms:** For new B2B AI tools that solve specific business problems, implying a use case.
6.  **Reports from Market Research Firms (if publicly accessible snippets are available):** Discussing AI adoption trends and specific applications.
7.  **Niche Online Communities/Forums:** Where SMB owners or industry professionals discuss adopting new technologies (e.g., certain subreddits, specialized forums).

**Information to Extract for Each Identified Business Use Case (Mandatory Fields):**

1.  **Use Case Title/Application Name:** (Clear, descriptive title).
2.  **Industry(s) Primarily Targeted/Affected:** (e.g., Retail, Healthcare, Marketing, Manufacturing, Professional Services).
3.  **Underlying AI Technology/Innovation Leveraged:** (Briefly describe the core AI enabling this, e.g., 'LLM-powered customer intent analysis,' 'AI vision for inventory management,' 'Generative AI for personalized sales collateral,' 'Agentic workflow automation').
4.  **Specific Business Problem Solved or Opportunity Addressed for Businesses (especially SMBs):**
5.  **Detailed Description of the AI Application/Workflow:** (How does it work in practice? What are the steps involved?)
6.  **Source(s) of Information:** (Direct URL(s) to case study, article, announcement, etc. Prioritize credible sources).
7.  **Monetization Strategy / Business Value for the End-User Business:** (How does the business using this AI make money, save money, or gain value? e.g., Increased sales, reduced operational costs, improved customer retention, new service offering).
8.  **Opportunity for an AI Agent Building Company (SMB Focus):**
    *   **Potential Managed Agent Service Offering:** (How could this use case be productized as a managed AI agent service for SMBs?)
    *   **Type of AI Agent(s) to Build:** (e.g., Customer service agent, data analysis agent, content creation agent, outbound sales agent).
    *   **Key Features of the Agent Solution:**
    *   **Value Proposition to SMB Clients:** (Why would an SMB pay for this managed agent?)
9.  **Monetization Model for the Agent Building Company:** (e.g., Subscription fee (tiered?), usage-based, setup fee + retainer, value-based pricing).
10. **Key Challenges & Considerations for SMB Implementation:** (e.g., Data requirements, integration with existing SMB tools, ease of use, initial cost, training).
11. **Evidence of Success/ROI (if available):** (Quantifiable results, testimonials, market adoption).
12. **Scalability & Adaptability:** (How easily can this use case be adapted for different SMBs or slightly different needs within the same sector?)
13. **Perceived Novelty/Innovation of this Business Application:** (Is this a truly new way of using AI in business, or a significant improvement on existing methods?)

**Output Format & Organization:**
*   Present findings as a list of distinct business use cases/applications.
*   For each item, use the exact field names listed above in a clear, structured format (e.g., using markdown headings or bolded labels for each field).
*   If few distinct, actionable examples are found, prioritize quality and depth over quantity.
*   Order the use cases by perceived relevance and opportunity for an SMB-focused AI agent building company.

**Analytical Guidance:**
*   Think like a product manager or solutions architect for the AI agent building company.
*   Focus on practicality, implementability, and clear value propositions for SMBs.
*   Connect the dots between a general AI innovation and a specific, monetizable business service.
*   Where possible, identify 'low-hanging fruit' or use cases with a lower barrier to entry for SMBs.

**Final Check:** Before reporting a use case, ask: 'Could an AI agent company realistically build and sell a managed service based on this to an SMB within the next 6-12 months? Does it solve a real pain point for SMBs?'

---

**Clarifying Questions I *Could* Ask (but the prompt aims to cover them):**

1.  *What specific types of 'agents' is the company building or looking to build?* (The prompt tries to keep this open but focuses on common business functions). If you have very specific agent types in mind (e.g., 'only customer service agents' or 'only data analysis agents'), we could narrow it.
2.  *Are there any specific industries the SMB clients are in that you want to prioritize?* (The prompt is general, but could be tailored).
3.  *What's the typical tech-savviness of the SMB clients?* (This influences the complexity of solutions they might adopt). The prompt assumes a need for 'managed' services, implying a desire for simplicity.
4.  *What is the acceptable timeframe for a 'new' innovation?* (I've put 'last 3-6 months' for the underlying tech, as business adoption often lags tech release).

This prompt structure should provide highly relevant and actionable insights for your podcast, specifically catering to the needs and perspective of an AI agent building company serving SMBs.
/llm/prompt/aibusiness
"""
]
if __name__ == "__main__":
    main(sys.argv[1:])  