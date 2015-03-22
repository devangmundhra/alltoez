// Generated by CoffeeScript 1.8.0
(function() {
  $(document).ready(function() {
    $.ajax({
      type: "GET",
      url: "" + similar_events_url,
      contentType: "application/html",
      dataType: "html",
      processData: false,
      error: function(jqXHR, textStatus, errorThrown) {
        return console.log("" + textStatus + " in getting similar events " + errorThrown);
      },
      success: function(data, textStatus, jqXHR) {
        return $(".similar-events-list").append(data);
      }
    });
    $('#bookmark-action').on("click", function(e) {
      if (myevent.bookmark) {
        return $.ajax({
          type: "DELETE",
          url: myevent.bookmark,
          contentType: "application/json",
          dataType: "html",
          processData: false,
          error: function(jqXHR, textStatus, errorThrown) {
            console.log("" + textStatus + " in unbookmarking " + errorThrown);
            $(e.target).button("toggle");
            return $(e.target).addClass("active");
          },
          success: function(data, textStatus, jqXHR) {
            return myevent.bookmark = "";
          }
        });
      } else {
        return $.ajax({
          type: "POST",
          url: "" + bookmark_url,
          data: JSON.stringify({
            "event": "" + myevent.resource_uri
          }),
          contentType: "application/json",
          dataType: "html",
          processData: false,
          error: function(jqXHR, textStatus, errorThrown) {
            console.log("" + textStatus + " in bookmarking event " + errorThrown);
            $(e.target).button("toggle");
            return $(e.target).removeClass("active");
          },
          success: function(data, textStatus, jqXHR) {
            var bookmark;
            bookmark = JSON.parse(data);
            return myevent.bookmark = bookmark.resource_uri;
          }
        });
      }
    });
    $('#done-action').on("click", function(e) {
      if (myevent.done) {
        return $.ajax({
          type: "DELETE",
          url: myevent.done,
          contentType: "application/json",
          dataType: "html",
          processData: false,
          error: function(jqXHR, textStatus, errorThrown) {
            console.log("" + textStatus + " in marking event undone " + errorThrown);
            $(e.target).button("toggle");
            return $(e.target).addClass("active");
          },
          success: function(data, textStatus, jqXHR) {
            return myevent.done = "";
          }
        });
      } else {
        return $.ajax({
          type: "POST",
          url: "" + done_url,
          data: JSON.stringify({
            "event": "" + myevent.resource_uri
          }),
          contentType: "application/json",
          dataType: "html",
          processData: false,
          error: function(jqXHR, textStatus, errorThrown) {
            console.log("" + textStatus + " in marking event done " + errorThrown);
            $(e.target).button("toggle");
            return $(e.target).removeClass("active");
          },
          success: function(data, textStatus, jqXHR) {
            var done;
            done = JSON.parse(data);
            return myevent.done = done.resource_uri;
          }
        });
      }
    });
    return $('#share-action').on("click", function(e) {
      if (!$(e.target).hasClass("active")) {
        return $('#share-info-dropdown').addClass("visible");
      } else {
        return $('#share-info-dropdown').removeClass("visible");
      }
    });
  });

}).call(this);
