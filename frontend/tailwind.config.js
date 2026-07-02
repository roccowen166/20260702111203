/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#ecf5ff',
          100: '#d9ecff',
          200: '#a0cfff',
          300: '#79bbff',
          400: '#409eff',
          500: '#337ecc',
          600: '#2670cc',
          700: '#1c5fb3',
          800: '#0d4a94',
          900: '#003a7a',
        },
      },
    },
  },
  corePlugins: {
    preflight: false,
  },
  plugins: [],
}
