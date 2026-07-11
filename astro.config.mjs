import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://olivershetler.github.io',
  output: 'static',
  integrations: [sitemap()],
});
