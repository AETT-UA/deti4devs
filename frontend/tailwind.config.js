/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'primary-color': '#262651',
        'secondary-color': '#EB7C29',
        'white-smoke': '#F5F5F5',
      },
    },
  },
  plugins: [
    require('daisyui')
  ],
}
