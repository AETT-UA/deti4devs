/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    colors: {
      "blue-primary": "#272654",
      "brown-primary": "#8B4615",
      "gray-primary": "#5F5F5F",
      "gray-secondary": "#5F5F5F99",
      "black-primary":"#292929",
      "white":"#FFFFFF",
    },
    extend: {

    },
  },
  plugins: [
    require('daisyui')
  ],
}
