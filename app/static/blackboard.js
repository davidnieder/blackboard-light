/* globals */
var $window;
var $contentSection;
var csrfToken;
var apiBase = '/api/posts';

/* prevent events from calling their handler unnecessary often
 * calls 'handler' on the first event if call_on is true (default)
 * calls 'handler' again after 'timeout' if 'call_after' is true
 */
function debounceEvent(event, handler) {
  /* default parameters */
  timeout = typeof timeout !== 'undefined' ? timeout : 500;
  call_on = typeof call_on !== 'undefined' ? call_on : true
  call_after = typeof call_after !== 'undefined' ? call_after : false;

  function fireOnce() {
    if (call_on)
      handler();
    $window.off(event);
  }
  $window.on(event, function()  {
    fireOnce();
    setTimeout(function() {
      debounceEvent(event, handler, call_on, call_after);
      if (call_after)
        handler();
    }, timeout);
  });
}

/* set new csrf-token after successful ajax requests */
function updateCsrfToken(event, xhr, settings)  {
  if (xhr.responseJSON && xhr.responseJSON.csrfToken) {
    csrfToken = xhr.responseJSON.csrfToken;
  }
}

/* manipulate page links */
function initPageLinks()  {
  /* prepare delete-post links */
  initDeleteLinks();
  /* hide prev-page/next-page links */
  $('#page-links').hide();
  /* show load-more-dynamic link, load-more event handler */
  $('#load-dynamic').show();
  if (nextPage) {
    $('#load-more-link').show();
    $('#load-more-link').find('a').on('click', loadMoreClicked);
    $('#load-more-error').find('a').on('click', loadMoreClicked);
  } else {
    $('#no-more-posts').show();
  }
  /* add click-event to scroll-to-top link */
  $('#no-more-posts').find('a').on('click', function(event)  {
    event.preventDefault();
    $("html, body").animate({scrollTop: 0}, 'slow');
  });
}

/* register click-event handler on all delete links */
function initDeleteLinks()  {
  var $deleteLinks = $('a[href^="/deletePost"]');
  $deleteLinks.off('click');
  $deleteLinks.on('click', deleteLinkClicked);
}

/* delete-link click-event handler */
function deleteLinkClicked(event) {
  event.preventDefault();
  var $link = $(event.target);

  /* prevent double clicking */
  if ($link.attr('disabled'))
    return;

  var postId = $link.attr('data-post-id');
  var $postContainer = $("#post-" + postId);
  var title = $postContainer.find('header:first').find('h4').text();
  var message = 'Do you want to delete post ';
  message += title ? '"'+title+'"?' : '#'+postId+'?';

  /* ask confirmation and delete post */
  if (confirm(message)) {
    $link.attr('disabled', true);
    deletePost(postId, $postContainer, $link);
  }
}

/* delete-post ajax request */
function deletePost(postId, $post, $link)  {
  $.ajax({
    url: apiBase,
    type: 'DELETE',
    contentType: 'application/json',
    processData: false,
    data: JSON.stringify({ postId: postId, csrfToken: csrfToken }),
    dataType: 'json',
    success: function(resp) {
      if (resp.success) {
        $post.fadeOut(1000);
        $post.remove();
      }
    },
    error: function(xhr, status, error) {
      var reason = xhr.status + ' ' + xhr.statusText;
      alert('Could not delete post. Reason: ' + reason);
      $link.attr('disabled', false);
    }
  });
}

/* window-scrolled event handler */
function windowScrolled() {
  if (postInView()) {
    $('#load-more-link').find('a').click()
  }
}

/* check if the second to last post is in browser view */
function postInView()  {
  var secondLastPost = $contentSection.find('article:nth-last-child(3)');
  if (secondLastPost.length == 0)
    return false;

  var postTop = secondLastPost.offset().top;
  var viewBottom = $window.scrollTop() + $window.height();
  return viewBottom >= postTop;
}

/* load-more-posts-link click-event handler */
function loadMoreClicked(event)  {
  event.preventDefault();
  if (nextPage != 0 && $.active == 0) {
    $('#load-more-link').hide();
    $('#load-more-error').hide();
    $('#loading-indicator').show();

    var query = postFilter;
    query.renderPosts = true;
    query.page = nextPage;
    loadPosts(query);
  }
}

/* load-more-posts ajax request */
function loadPosts(query)  {
  $.ajax({
    url: apiBase,
    type: 'GET',
    processData: true,
    data: query,
    dataType: 'json',
    success: loadedPosts,
    error: loadPostsError,
    complete: function()  {
      $('#loading-indicator').hide();
    }
  });
}

/* load-more-posts success callback */
function loadedPosts(resp)  {
  /* insert new posts into dom */
  for (var post of resp.postList) {
    $contentSection.find('hr:last').before(post);
  }
  if (resp.hasMore)   {
    /* for next request */
    nextPage++;
    $('#load-more-link').show();
  } else {
    /* there are no more posts */
    nextPage = 0;
    //$('#load-more-link').hide();
    $('#no-more-posts').show();
  }
  /* prepare new delete links */
  initDeleteLinks();
  $('#load-more-error').hide()
}

/* load-more-posts error callback */
function loadPostsError(xhr, status, error) {
  var msg = $('#load-more-error span');
  if (error)  {
    msg.text('Could not load posts (' + error.toLowerCase() + ').');
  } else {
    msg.text('Could not load posts.');
  }
  msg.show();
  $('#load-more-error').show();
}

/* add script functionality to page */
function initPage() {
  $window = $(window);
  $contentSection = $('#content');
  csrfToken = $('meta[name="csrf_token"]').attr('value');

  /* prepare page links */
  initPageLinks();

  /* update csrf token after ajax requests */
  $(document).on('ajaxSuccess', updateCsrfToken);

  /* register page-scrolled handler */
  debounceEvent('scroll', windowScrolled, call_on=false, call_after=true);
  /* if there are no scroll bars, load more posts now */
  windowScrolled();
}
