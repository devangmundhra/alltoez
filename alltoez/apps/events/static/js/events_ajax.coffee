$('#bookmark-action').on "click", (e) ->
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
      data: JSON.stringify {"event":"#{myevent.resource_uri}"}
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
  if myevent.done
    $.ajax
      type: "DELETE"
      url: myevent.done
      contentType: "application/json"
      dataType: "html"
      processData: false
      error: (jqXHR, textStatus, errorThrown) ->
        console.log "#{textStatus} in marking event undone #{errorThrown}"
        $( e.target ).button "toggle"
        $( e.target ).addClass "active"
      success: (data, textStatus, jqXHR) ->
        myevent.done = ""
  else
    $.ajax
      type: "POST"
      url: "#{done_url}"
      data: JSON.stringify {"event":"#{myevent.resource_uri}"}
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
