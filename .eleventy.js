const Image = require("@11ty/eleventy-img");
// const { eleventyImageTransformPlugin } = require("@11ty/eleventy-img");

// (async () => {
// 	let url = "https://images.unsplash.com/photo-1608178398319-48f814d0750c";
// 	let stats = await Image(url, {
// 		widths: [300],
//     // Array of file format extensions or "auto"
// 		formats: ["webp", "jpeg"],
// 	});

// 	console.log(stats);
// })();

module.exports = function (eleventyConfig) {
  eleventyConfig.addPassthroughCopy("./src/css");
  eleventyConfig.addPassthroughCopy("./src/img");
  eleventyConfig.addPassthroughCopy("./src/fonts");
  eleventyConfig.addPassthroughCopy("./src/js");

//   eleventyConfig.addPlugin(eleventyImageTransformPlugin, {
// 		// which file extensions to process
// 		extensions: "html",

// 		// Add any other Image utility options here:

// 		// optional, output image formats
// 		formats: ["webp", "jpeg"],
// 		// formats: ["auto"],

// 		// optional, output image widths
// 		// widths: ["auto"],

//     outputDir: './public/img/',
//     urlPath: '/src/img/',

// 		// optional, attributes assigned on <img> override these values.
// 		defaultAttributes: {
// 			loading: "lazy",
// 			decoding: "async",
// 		},
// 	});

  return {
    dir: {
      input: "src",
      output: "public",
      includes: "_includes",
    },
  };
};