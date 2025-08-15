const pluginRss = require("@11ty/eleventy-plugin-rss");

// const path = require("path");
// const eleventyImage = require("@11ty/eleventy-img");
// const { eleventyImageTransformPlugin } = require("@11ty/eleventy-img");

module.exports = function (eleventyConfig) {
  // PASSTHROUGH COPIES ------------------------------------------------------------------- //
  eleventyConfig.addPassthroughCopy("./src/css");
  eleventyConfig.addPassthroughCopy("./src/img");
  eleventyConfig.addPassthroughCopy("./src/vid");
  eleventyConfig.addPassthroughCopy("./src/js");
  eleventyConfig.addPassthroughCopy("./src/rss");
  eleventyConfig.addPassthroughCopy("./src/robots.txt");
  
  eleventyConfig.addPassthroughCopy("./src/assets");
  eleventyConfig.addPassthroughCopy("./src/writing/an-experiment");

  // RSS
  eleventyConfig.addPlugin(pluginRss);

  /** COLLECTION FILTERING AND SORTING ------------------------------------- */

  // when tags are spoilers and NO SPOILERS, gonna end up with nothing!
  // However, can use this for having:
  // - split TWEWY OG, NEO 
  // - also have them ALL combined!
  eleventyConfig.addCollection("allTWEWY", function (collectionApi) {
    // ge filtered by Tags - is requiring BOTH tags - so good for spoiler tagging? 
    return collectionApi.getFilteredByTags("twewyArt2All", "twewyArtNoSpoilers");
  });

  // SORTING ------------------------------------------------------------------- // 
  // Sort by TITLE
  eleventyConfig.addCollection("twewySeriesArtAllByTitle", (collection) =>
    collection.getFilteredByTags("twewyArt2").sort((a, b) => {
      let nameA = a.data.twewyart.title.toUpperCase();
      let nameB = b.data.twewyart.title.toUpperCase();
      if (nameA < nameB) return -1;
      else if (nameA > nameB) return 1;
      else return 0;
    })
  );

  // Sort by DATE
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

  // Sort by DATE
  // OG TWEWY
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

  // NEO TWEWY
  eleventyConfig.addCollection("twewyNEOArtAllByDate", function (collectionApi) {
    // ge filtered by Tags - is requiring BOTH tags - so good for spoiler tagging? 
    return collectionApi.getFilteredByTags("twewyNeoArt").sort(function (a, b) {
      let nameA = a.data.twewyart.date.toUpperCase();
      let nameB = b.data.twewyart.date.toUpperCase();
      if (nameA > nameB) return -1;
      else if (nameA < nameB) return 1;
      else return 0;
    });
  });

   // PERSONA 5 - Sort by DATE
   eleventyConfig.addCollection("Persona5ByDateCollection", function (collectionApi) {
    // ge filtered by Tags - is requiring BOTH tags - so good for spoiler tagging? 
    return collectionApi.getFilteredByTags("TagPersona5Art").sort(function (a, b) {
      let nameA = a.data.aArtwork.date.toUpperCase();
      let nameB = b.data.aArtwork.date.toUpperCase();
      if (nameA > nameB) return -1;
      else if (nameA < nameB) return 1;
      else return 0;
    });
  });


  // Filter artwork to get the most recently added ones
  eleventyConfig.addCollection("RecentArtwork", function (collectionApi) {
    // Get URLs from the latest 3 Update post into an array
    var urlArr = [];
    let artworkList;
    for (let k= 0; k < 3; k++) {
      artworkList = collectionApi.getFilteredByTags("UpdatePosts")[k].data.posts.ArtList;
      for (let i = 0; i < artworkList.length; i++) {
        for (let j = 0; j < artworkList[i].List.length; j++) {
          urlArr.push(artworkList[i].List[j].URL);
        }
      } 
    }

    // ge filtered by Tags - is requiring BOTH tags - so good for spoiler tagging? 
    return collectionApi.getFilteredByTags("MyArt").filter(function (item) {
			// Only return content that was originally a markdown file
			let artworkURL = item.page.url;
			return urlArr.includes(artworkURL);
		});
  });

  // RETURN ------------------------------------------------------------------- //
  return {
    dir: {
      input: "src",
      output: "public",
      includes: "_includes",
    },
  };
};