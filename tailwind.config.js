/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["render/templates/**/*.{html,js}"],
  theme: {
    extend: {},
  },
  plugins: [require("@tailwindcss/typography"), require("daisyui")],
}
