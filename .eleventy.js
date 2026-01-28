const pluginRss = require("@11ty/eleventy-plugin-rss");

const utilsTemp = require("util");

// const path = require("path");
// const eleventyImage = require("@11ty/eleventy-img");
// const { eleventyImageTransformPlugin } = require("@11ty/eleventy-img");

function sortaArtworkDate(a, b) {
  let nameA = a.data.aArtwork.date.toUpperCase();
  let nameB = b.data.aArtwork.date.toUpperCase();
  if (nameA > nameB) return -1;
  else if (nameA < nameB) return 1;
  else return 0;
};

function sortaArtworkWebsiteDate(a, b) {
  let dateA = a.data.aArtwork.WebsiteDateUTC;
  let dateB = b.data.aArtwork.WebsiteDateUTC;
  if (dateA > dateB) return -1;
  else if (dateA < dateB) return 1;
  else return 0;
};


function sortByHeader(a, b) {
  let dateA = a.data.mainGrouping;
  let dateB = b.data.mainGrouping;
  if (dateA < dateB) return -1;
  else if (dateA > dateB) return 1;
  else return 0;
}


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
    collection.getFilteredByTags("aArtwork").sort((a, b) => {
      let nameA = a.data.aArtwork.title.toUpperCase();
      let nameB = b.data.aArtwork.title.toUpperCase();
      if (nameA < nameB) return -1;
      else if (nameA > nameB) return 1;
      else return 0;
    })
  );

  // Sort by DATE
  eleventyConfig.addCollection("twewySeriesArtAllByDate", function (collectionApi) {
    // ge filtered by Tags - is requiring BOTH tags - so good for spoiler tagging? 
    return collectionApi.getFilteredByTags("twewyArt2").sort(function (a, b) {

      let nameA = a.data.aArtwork.date.toUpperCase();
      let nameB = b.data.aArtwork.date.toUpperCase();
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
      let nameA = a.data.aArtwork.date.toUpperCase();
      let nameB = b.data.aArtwork.date.toUpperCase();
      if (nameA > nameB) return -1;
      else if (nameA < nameB) return 1;
      else return 0;
    });
  });

  // NEO TWEWY
  eleventyConfig.addCollection("twewyNEOArtAllByDate", function (collectionApi) {
    // ge filtered by Tags - is requiring BOTH tags - so good for spoiler tagging? 
    return collectionApi.getFilteredByTags("twewyNeoArt").sort(function (a, b) {
      let nameA = a.data.aArtwork.date.toUpperCase();
      let nameB = b.data.aArtwork.date.toUpperCase();
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


  // Fandom ------------------------------------------------------------------------ // 
  eleventyConfig.addCollection("fandomArtworkSorted", function (collectionApi) {
    return collectionApi.getFilteredByTags("fandomArtwork")
      .sort(sortByHeader);
  });

  // Filter artwork to get the most recently added ones
  eleventyConfig.addCollection("RecentArtwork", function (collectionApi) {
    // Get URLs from the latest 3 Update post into an array
    var urlArr = [];
    let artworkList;
    for (let k= 0; k < 5; k++) {
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
		}).sort(sortaArtworkWebsiteDate);
  });

  // Filter artwork to get the most recently added ones
  eleventyConfig.addCollection("RecentArtworkNoSpoilers", function (collectionApi) {
    // Get URLs from the latest 3 Update post into an array
    var urlArr = [];
    let artworkList;
    for (let k= 0; k < 5; k++) {
      artworkList = collectionApi.getFilteredByTags("UpdatePosts")[k].data.posts.ArtList;
      for (let i = 0; i < artworkList.length; i++) {
        for (let j = 0; j < artworkList[i].List.length; j++) {
          urlArr.push(artworkList[i].List[j].URL);
        }
      } 
    }

    // ge filtered by Tags - is requiring BOTH tags - so good for spoiler tagging? 
    return collectionApi.getFilteredByTags("MyArt")
      .filter(function (item) {
        // Only return content that was originally a markdown file
        let artworkURL = item.page.url;
        return urlArr.includes(artworkURL )&& item.data.aArtwork.spoilers.toUpperCase() === "NO";
		  })
      .sort(sortaArtworkWebsiteDate);
  });

  // BAsed on when the were posted online, not to the site
  eleventyConfig.addCollection("RecentArtworkPostDate", function (collectionApi) {
    // Sort by artwork actual posted date on the intermets
    return collectionApi.getFilteredByTags("MyArt").sort(function (a, b) {
      let nameA = a.data.aArtwork.date.toUpperCase();
      let nameB = b.data.aArtwork.date.toUpperCase();
      if (nameA > nameB) return -1;
      else if (nameA < nameB) return 1;
      else return 0;
    });
  });

  // BAsed on when the were posted online, not to the site
  eleventyConfig.addCollection("RecentArtworkPostDateNoSpoilers", function (collectionApi) {
    // Sort by artwork actual posted date on the intermets
    return collectionApi.getFilteredByTags("MyArt")
    .filter(function (item) { 
        return item.data.aArtwork.spoilers.toUpperCase() === "NO";
      })
    .sort(function (a, b) {
      let nameA = a.data.aArtwork.date.toUpperCase();
      let nameB = b.data.aArtwork.date.toUpperCase();
      if (nameA > nameB) return -1;
      else if (nameA < nameB) return 1;
      else return 0;
    });
  });


  eleventyConfig.addFilter("dump", (obj) => {
    return utilsTemp.inspect(obj);
  });

  // MISC -----------------------------------------//

  eleventyConfig.addCollection("RSSFeed", function (collectionApi) {
    return collectionApi.getFilteredByTags("UpdatePosts").slice(0,6);
  });

  // FANDOMS -------------------------------------- //

  // OCs
  eleventyConfig.addCollection("OCArt", function (collectionApi) {
    return collectionApi.getFilteredByTags("MyArt").filter(function (item) {
			return item.data.aArtwork.fandom.includes("OC") || item.data.aArtwork.oc.toUpperCase() === "YES";
    })
    .sort(sortaArtworkDate);
  });

  // OCs
  eleventyConfig.addCollection("OCArtNoSpoilers", function (collectionApi) {
    return collectionApi.getFilteredByTags("MyArt").filter(function (item) {
			return (item.data.aArtwork.fandom.includes("OC") || item.data.aArtwork.oc.toUpperCase() === "YES") && item.data.aArtwork.spoilers.toUpperCase() === "NO";
    })
    .sort(sortaArtworkDate);
  });

  // Art Fight --------------------------------------------------------------- //
  eleventyConfig.addCollection("ArtFightNoSpoilers", function (collectionApi) {
    return collectionApi.getFilteredByTags("MyArt")
      .filter(function (item) { 
        return item.data.aArtwork.fandom.includes("ArtFight") && item.data.aArtwork.spoilers.toUpperCase() === "NO";
      })
      .sort(sortaArtworkDate);
  });

  eleventyConfig.addCollection("AsurasWrathNoSpoilers", function (collectionApi) {
    return collectionApi.getFilteredByTags("MyArt")
      .filter(function (item) { 
        return item.data.aArtwork.fandom.includes("asuras-wrath") && item.data.aArtwork.spoilers.toUpperCase() === "NO";
      })
      .sort(sortaArtworkDate);
  });

  eleventyConfig.addCollection("DeltaruneArt", function (collectionApi) {
    return collectionApi.getFilteredByTags("MyArt").filter(function (item) {
			return item.data.aArtwork.fandom.includes("Deltarune");
    })
    .sort(sortaArtworkDate);
  });

  eleventyConfig.addCollection("KirbyArtNoSpoilers", function (collectionApi) {
    return collectionApi.getFilteredByTags("MyArt").filter(function (item) {
			return item.data.aArtwork.fandom.includes("Kirby") && item.data.aArtwork.spoilers.toUpperCase() === "NO";
    })
    .sort(sortaArtworkDate);
  });

  eleventyConfig.addCollection("LaMulanaArtNoSpoilers", function (collectionApi) {
    return collectionApi.getFilteredByTags("MyArt").filter(function (item) {
			return item.data.aArtwork.fandom.includes("LaMulana") && item.data.aArtwork.spoilers.toUpperCase() === "NO";
    })
    .sort(sortaArtworkDate);
  });

  // Persona 5
  eleventyConfig.addCollection("Persona5ArtNoSpoilers", function (collectionApi) {
    return collectionApi.getFilteredByTags("MyArt")
      .filter(function (item) {
			  return item.data.aArtwork.fandom.includes("persona5") && item.data.aArtwork.spoilers.toUpperCase() === "NO";
      })
      .sort(sortaArtworkDate)
  });

  eleventyConfig.addCollection("Persona5Art", function (collectionApi) {
    return collectionApi.getFilteredByTags("MyArt")
      .filter(function (item) {
        return item.data.aArtwork.fandom.includes("persona5");
      })
      .sort(sortaArtworkDate)
  });

  // Pikmin
  eleventyConfig.addCollection("PikminArt", function (collectionApi) {
    return collectionApi.getFilteredByTags("MyArt").filter(function (item) {
			return item.data.aArtwork.fandom.includes("Pikmin");
    })
    .sort(sortaArtworkDate);
  });

  eleventyConfig.addCollection("PokemonArtNoSpoilers", function (collectionApi) {
    return collectionApi.getFilteredByTags("MyArt").filter(function (item) {
			return item.data.aArtwork.fandom.includes("Pokemon") && item.data.aArtwork.spoilers.toUpperCase() === "NO";
    })
    .sort(sortaArtworkDate);
  });

  // Project Moon
  eleventyConfig.addCollection("ProjectMoonArt", function (collectionApi) {
    return collectionApi.getFilteredByTags("MyArt")
      .filter(function (item) {
        return item.data.aArtwork.fandom.includes("ProjectMoon");
      })
      .sort(sortaArtworkDate);
  });

  // Super Puzzled Cat
  eleventyConfig.addCollection("SuperPuzzledCatArt", function (collectionApi) {
    return collectionApi.getFilteredByTags("MyArt").filter(function (item) {
			return item.data.aArtwork.fandom.includes("super-puzzled-cat");
    })
    .sort(sortaArtworkDate);
  });

  // Splatoon
  eleventyConfig.addCollection("SplatoonArt", function (collectionApi) {
    return collectionApi.getFilteredByTags("MyArt").filter(function (item) {
			return item.data.aArtwork.fandom.includes("Splatoon");
    })
    .sort(sortaArtworkDate);
  });

  // Splatoon
  eleventyConfig.addCollection("SplatoonArtNoSpoilers", function (collectionApi) {
    return collectionApi.getFilteredByTags("MyArt").filter(function (item) {
			return item.data.aArtwork.fandom.includes("Splatoon") &&  item.data.aArtwork.spoilers.toUpperCase() === "NO";
    })
    .sort(sortaArtworkDate);
  });

  // TWEWY Series ------------------------------------------------------------//
  eleventyConfig.addCollection("TWEWYSeriesArt", function (collectionApi) {
    return collectionApi.getFilteredByTags("MyArt")
      .filter(function (item) { 
        return item.data.aArtwork.fandom.includes("TWEWY") || item.data.aArtwork.fandom.includes("NTWEWY");
      })
      .sort(sortaArtworkDate);
  });

  // Series No Spoilers
  eleventyConfig.addCollection("TWEWYSeriesArtNoSpoilers", function (collectionApi) {
    return collectionApi.getFilteredByTags("MyArt")
      .filter(function (item) { 
        return (item.data.aArtwork.fandom.includes("TWEWY") || item.data.aArtwork.fandom.includes("NTWEWY")) &&  item.data.aArtwork.spoilers.toUpperCase() === "NO";
      })
      .sort(sortaArtworkDate);
  });

  // TWEWY - OG
  eleventyConfig.addCollection("TWEWYArt", function (collectionApi) {
    return collectionApi.getFilteredByTags("MyArt")
      .filter(function (item) { 
        return item.data.aArtwork.fandom.includes("TWEWY");
      })
      .sort(sortaArtworkDate);
  });

   // TWEWY - OG, no spoilers
  eleventyConfig.addCollection("TWEWYArtNoSpoilers", function (collectionApi) {
    return collectionApi.getFilteredByTags("MyArt")
      .filter(function (item) { 
        return item.data.aArtwork.fandom.includes("TWEWY") && item.data.aArtwork.spoilers.toUpperCase() === "NO";
      })
      .sort(sortaArtworkDate);
  });

  // TWEWY - NEO
  eleventyConfig.addCollection("NEOTWEWYArt", function (collectionApi) {
    return collectionApi.getFilteredByTags("MyArt")
      .filter(function (item) { 
        return item.data.aArtwork.fandom.includes("NTWEWY")
      })
      .sort(sortaArtworkDate);
  });

   // TWEWY - NEO, no spoilers
  eleventyConfig.addCollection("NEOTWEWYArtNoSpoilers", function (collectionApi) {
    return collectionApi.getFilteredByTags("MyArt")
      .filter(function (item) { 
        return item.data.aArtwork.fandom.includes("NTWEWY") && item.data.aArtwork.spoilers.toUpperCase() === "NO";
      })
      .sort(sortaArtworkDate);
  });
  // -------------------------------------------------------------------------- //

  // Void Stranger
  eleventyConfig.addCollection("VoidStrangerArtNoSpoilers", function (collectionApi) {
    return collectionApi.getFilteredByTags("MyArt").filter(function (item) {
			return item.data.aArtwork.fandom.includes("VoidStranger") && item.data.aArtwork.spoilers.toUpperCase() === "NO";
    })
    .sort(sortaArtworkDate);
  });

  eleventyConfig.addCollection("VoidStrangerArt", function (collectionApi) {
    return collectionApi.getFilteredByTags("MyArt").filter(function (item) {
			return item.data.aArtwork.fandom.includes("VoidStranger");
    })
    .sort(sortaArtworkDate);
  });

  eleventyConfig.addCollection("XCXArtNoSpoilers", function (collectionApi) {
    return collectionApi.getFilteredByTags("MyArt")
      .filter(function (item) { 
        return item.data.aArtwork.fandom.includes("XCX") && item.data.aArtwork.spoilers.toUpperCase() === "NO";
      })
      .sort(sortaArtworkDate);
  });

   eleventyConfig.addCollection("XCXArt", function (collectionApi) {
    return collectionApi.getFilteredByTags("MyArt")
      .filter(function (item) { 
        return item.data.aArtwork.fandom.includes("XCX");
      })
      .sort(sortaArtworkDate);
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