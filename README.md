This is the server that serves [my personal website](https://github.com/nicbou/nicolasbouliane.com). It's a reference implementation of a server that serves an [Ursus](https://github.com/nicbou/ursus) website.

## How to use

Create a file called `.env` with the right environment variables. Use `.env.example` as a reference.

### Locally

Run `docker-compose up --build -d` in the project's root directory. It will serve the contents of `STATIC_SITE_PATH` (from your `.env` file) at `https://localhost`.

### In production

A production configuration is available. It includes the `ursus_builder` image, which rebuilds the website when there are new commits to the `nicolasbouliane.com` repo. Uncomment the `COMPOSE_FILE=...` line in your `.env` file to enable the production configuration.