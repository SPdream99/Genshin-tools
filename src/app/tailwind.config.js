/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/*.html",
    "./templates/Errors/*.html",
    "./static/src/**/*.{html,js}",
    "./static/node_modules/tw-elements/dist/js/**/*.js"
  ],
  plugins: [require("tw-elements/dist/plugin")],
  darkMode: "class"
};