module.exports = {
  daemon: true,
  run: [
    {
      method: "shell.run",
      params: {
        message: "python app.py {{encodeURIComponent(args.feature)}}",
        path: "app",
        venv: "env",
      },
    },
    {
      method: "notify",
      params: {
        html: "Features have been successfully started!",
      },
    },
  ],
};


