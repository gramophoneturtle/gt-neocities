const Image = require("@11ty/eleventy-img");
const path = require('path')

module.exports = function (eleventyConfig) {
  // --- PASS HROUGHS
  eleventyConfig.addPassthroughCopy("./src/css");
  eleventyConfig.addPassthroughCopy("./src/img");
  eleventyConfig.addPassthroughCopy("./src/fonts");
  eleventyConfig.addPassthroughCopy("./src/js");
  eleventyConfig.addPassthroughCopy("./src/robots.txt");

  // -- START, eleventy-img
	function imageShortcode(src, alt, sizes="(min-width: 1024px) 100vw, 50vw") {
		console.log(`Generating image(s) from:  ${src}`)
		let options = {
			widths: [600, 900, 1500],
			formats: ["webp", "jpeg","png"],
			urlPath: "/img/",
			outputDir: "./public/img/",

			filenameFormat: function (id, src, width, format, options) {
        const extension = path.extname(src)
				const name = path.basename(src, extension)

        console.log(`filenameFormat src:  ${src}`)

        
        let tmpPath = path.dirname(src)
		    console.log(`> filenameFormat path:  ${tmpPath}`)
        
        tmpPath = tmpPath.replace("./src/img/","")
		    console.log(`> 2  filenameFormat path:  ${tmpPath}`)
		    console.log(`> 3 proper? filenameFormat Creating:  ${tmpPath}/${name}-${width}w.${format}`)
        
        let newFilanme = tmpPath + '/' + name + '-'+ width +'w.' + format;

        // tmpPath = path.normalize(path.format({dir: tmpPath, name:newFilanme, ext: format}))
		    // console.log(`> 4 proper filenameFormat path:  ${tmpPath}`)


		    console.log(`OG filenameFormat Creating:  ${name}-${width}w.${format}`)

        console.log(newFilanme)
        return newFilanme
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