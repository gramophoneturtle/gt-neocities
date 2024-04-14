const Image = require("@11ty/eleventy-img");
const path = require('path')

// (async () => {
// 	let url = "";
// 	let stats = await Image(url, {
// 		widths: [300, 600, auto],
//     // Array of file format extensions or "auto"
// 		formats: ["webp", "jpeg"],

//     outputDir: "./public/img/"

// 	});

// 	console.log(stats);
// })();

// ex for custom filename - goes here?
// const path = require("path");
// const Image = require("@11ty/eleventy-img");

// await Image("./test/bio-2017.jpg", {
// 	widths: [300],
// 	formats: ["auto"],
// 	filenameFormat: function (id, src, width, format, options) {
// 		const extension = path.extname(src);
// 		const name = path.basename(src, extension);

// 		return `${name}-${width}w.${format}`;
// 	},
// });

module.exports = function (eleventyConfig) {
  // --- PASS HROUGHS
  eleventyConfig.addPassthroughCopy("./src/css");
  eleventyConfig.addPassthroughCopy("./src/img");
  eleventyConfig.addPassthroughCopy("./src/fonts");
  eleventyConfig.addPassthroughCopy("./src/js");
  eleventyConfig.addPassthroughCopy("./src/robots.txt");

  // --- START, eleventy-img
	function imageShortcode(src, alt, sizes="(min-width: 1024px) 100vw, 50vw") {
		console.log(`Generating image(s) from:  ${src}`)
		let options = {
			widths: [200, 800, 1500],
			formats: ["webp", "jpeg"],
			urlPath: "./src/img/",
			outputDir: "./public/img/",
			filenameFormat: function (id, src, width, format, options) {
				const extension = path.extname(src)
				const name = path.basename(src, extension)
				return `${name}-${width}w.${format}`
			}
		}

		// generate images
		Image(src, options)

		let imageAttributes = {
			alt,
			sizes,
			loading: "lazy",
			decoding: "async",
		}
		// get metadata
		metadata = Image.statsSync(src, options)
		return Image.generateHTML(metadata, imageAttributes)
	}
	eleventyConfig.addShortcode("image", imageShortcode)
	// --- END, eleventy-img


  // shortcode test
   // ADD THIS
   eleventyConfig.addShortcode(
    "headers",
    (title, subtitle) =>
      `<h1>${title}</h1>
        <p>${subtitle}</p>`
  );

  // --- RETURN
  return {
    dir: {
      input: "src",
      output: "public",
      includes: "_includes",
    },
  };
};