$(document).ready ->
  isLoggedIn = window.isLoggedIn
  $.ajax
    type: "GET"
    url: "#{similar_events_url}"
    contentType: "application/html"
    dataType: "html"
    processData: false
    error: (jqXHR, textStatus, errorThrown) ->
      console.log "#{textStatus} in getting similar events #{errorThrown}"
    success: (data, textStatus, jqXHR) ->
      $(".similar-events-list").append data

  $('#bookmark-action').on "click", (e) ->
    if isLoggedIn
      if myevent.bookmark
        $.ajax
          type: "DELETE"
          url: myevent.bookmark
          contentType: "application/json"
          dataType: "html"
          processData: false
          error: (jqXHR, textStatus, errorThrown) ->
            console.log "#{textStatus} in unbookmarking #{errorThrown}"
            $( e.target ).button "toggle"
            $( e.target ).addClass "active"
          success: (data, textStatus, jqXHR) ->
            myevent.bookmark = ""
      else
        $.ajax
          type: "POST"
          url: "#{bookmark_url}"
          data: JSON.stringify {"event":"#{myevent.pk}"}
          contentType: "application/json"
          dataType: "html"
          processData: false
          error: (jqXHR, textStatus, errorThrown) ->
            console.log "#{textStatus} in bookmarking event #{errorThrown}"
            $( e.target ).button "toggle"
            $( e.target ).removeClass "active"
          success: (data, textStatus, jqXHR) ->
            bookmark = JSON.parse data
            myevent.bookmark = bookmark.resource_uri

  $('#done-action').on "click", (e) ->
    if isLoggedIn
      if not myevent.done
      #   $.ajax
      #     type: "DELETE"
      #     url: myevent.done
      #     contentType: "application/json"
      #     dataType: "html"
      #     processData: false
      #     error: (jqXHR, textStatus, errorThrown) ->
      #       console.log "#{textStatus} in marking event undone #{errorThrown}"
      #       $( e.target ).button "toggle"
      #       $( e.target ).addClass "active"
      #     success: (data, textStatus, jqXHR) ->
      #       myevent.done = ""
      # else
        $.ajax
          type: "POST"
          url: "#{done_url}"
          data: JSON.stringify {"event":"#{myevent.pk}"}
          contentType: "application/json"
          dataType: "html"
          processData: false
          error: (jqXHR, textStatus, errorThrown) ->
            console.log "#{textStatus} in marking event done #{errorThrown}"
            $( e.target ).button "toggle"
            $( e.target ).removeClass "active"
          success: (data, textStatus, jqXHR) ->
            done = JSON.parse data
            myevent.done = done.resource_uri

  $('#share-action').on "click", (e)->
    if not $( e.target ).hasClass "active"
      $('#share-info-dropdown').addClass "visible"
    else
      $('#share-info-dropdown').removeClass "visible"
