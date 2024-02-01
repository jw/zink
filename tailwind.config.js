/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["core/templates/**/*.{html,js}"],
  theme: {
    extend: {},
  },
  plugins: [require("@tailwindcss/typography"), require("daisyui")],
}
