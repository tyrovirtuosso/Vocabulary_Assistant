/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./Tyro2Virtuoso/**/*.{html,js}"],
  plugins: [
    require('@tailwindcss/typography'),
    // require("daisyui"),
    require('@tailwindcss/forms')
  ],
  // daisyui: {
  //   themes: false,
  //   darkTheme: "dark",
  //   base: true,
  //   styled: true,
  //   utils: true,
  // },
}