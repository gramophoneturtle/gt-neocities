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
  eleventyConfig.addPassthroughCopy("./src/robots.txt");



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

  // when tags are spoilers and NO SPOILERS, gonna end up with nothing!
  // However, can use this for spliting TWEWY OG, NEO and ALL
  eleventyConfig.addCollection("allTWEWY", function (collectionApi) {
    // ge filtered by Tags - is requiring BOTH tags - so good for spoiler tagging? 
    return collectionApi.getFilteredByTags("twewyArt2All", "twewyArtNoSpoilers");
  });

  eleventyConfig.addCollection("twewySeriesArtAllByTitle", (collection) =>
    collection.getFilteredByTags("twewyArt2").sort((a, b) => {
      let nameA = a.data.twewyart.title.toUpperCase();
      let nameB = b.data.twewyart.title.toUpperCase();
      if (nameA < nameB) return -1;
      else if (nameA > nameB) return 1;
      else return 0;
    })
  );

  eleventyConfig.addCollection("twewySeriesArtAllByDate", function (collectionApi) {
    // ge filtered by Tags - is requiring BOTH tags - so good for spoiler tagging? 
    return collectionApi.getFilteredByTags("twewyArt2").sort(function (a, b) {

      let nameA = a.data.twewyart.date.toUpperCase();
      let nameB = b.data.twewyart.date.toUpperCase();
      if (nameA > nameB) return -1;
      else if (nameA < nameB) return 1;
      else return 0;

    });
  });

  eleventyConfig.addCollection("twewyOGArtAllByDate", function (collectionApi) {
    // ge filtered by Tags - is requiring BOTH tags - so good for spoiler tagging? 
    return collectionApi.getFilteredByTags("twewyOGArt").sort(function (a, b) {

      let nameA = a.data.twewyart.date.toUpperCase();
      let nameB = b.data.twewyart.date.toUpperCase();
      if (nameA > nameB) return -1;
      else if (nameA < nameB) return 1;
      else return 0;

    });
  });


  return {
    dir: {
      input: "src",
      output: "public",
      includes: "_includes",
    },
  };
};