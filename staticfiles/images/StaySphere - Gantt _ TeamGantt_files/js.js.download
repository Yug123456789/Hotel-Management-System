// JavaScript Document

/* GET ELEMENT BY ID */
function $id(id) {
  return document.getElementById(id);
}

function $create(tag) {
  return document.createElement(tag);
}

function $text(string) {
  return document.createTextNode(string);
}

function $fragment() {
  return document.createDocumentFragment();
}

function json_decode(string) {
  return JSON.parse(string);
}

function subdomain(prefix) {
  var subdomain = window.location.host.split('.')[0];
  var parts = subdomain.split('-');

  if (parts[1]) {
    return prefix + '-' + parts[1];
  }

  return prefix;
}

function go_home() {
  var dir = $id('js_gantt_url') ? $id('js_gantt_url').value : 'gantt';
  var directory =
    $id('home_dir') && $id('home_dir').value != ''
      ? $id('home_dir').value
      : 'home/';
  navigate_window('/' + dir + '/' + directory);
}

function set_current_page_to_home() {
  // only save path after the /gantt directory
  var page = window.location.href.split('/gantt/')[1];
  set_home(page);
  close_user_icon_details();
  custom_alert('Your homepage has been successfully updated');
}

function set_home(page) {
  //PAGE CORRECTION
  if (page == 'my-list/') {
    var url = window.location.href;
    var u_split = url.split('/' + $id('js_gantt_url').value + '/');
    var page = u_split[1];

    //remove project_ids
    var url_parts = page.split('#');
    var keys = url_parts[1].split('&');
    var new_queryString = '';
    for (var k = 0; k < keys.length; k++) {
      if (keys[k].indexOf('ids') == 0) {
        //skip
      } else {
        new_queryString += new_queryString == '' ? '' : '&';
        new_queryString += keys[k];
      }
    }

    page = 'list/?ids=MY-ACTIVE&long_header=true#' + new_queryString;
  } else if (page == 'calendar/') {
    page = page + window.location.hash;
  }

  update_preference_new({
    key: 'app.web.homepage',
    type: 'string',
    value: page,
  });
  $id('home_dir').value = page;
}

/* Z-INDEX ADJUST */
function bring_to_front(ele) {
  var eles = document.body.getElementsByTagName('*');
  var highest = 0;
  var high = '';
  var len = eles.length;
  for (var i = 0; i < len; i++) {
    var zindex1 = getComputedStyle(eles[i]).zIndex * 1;
    var zindex2 = eles[i].style.zIndex * 1;
    var zindex = zindex1 > zindex2 ? zindex1 : zindex2;
    if (
      zindex > highest &&
      zindex != 'auto' &&
      getComputedStyle(eles[i]).display != 'none'
    ) {
      if (eles[i].id.indexOf('intercom') > -1) {
        //SKIP INTERCOM
      } else {
        highest = zindex;
        //high = zindex + " " + getComputedStyle(eles[i]).display + " " + eles[i].innerHTML + " " + eles[i].id;
      }
    }
  }
  ele.style.zIndex = highest * 1 + 1;
  return highest;
}

/* SIDEBAR */
function sidebar_width() {
  if (!document.getElementById('sidebar')) {
    return 0;
  }

  return 75;
}

function sidebar_check_size() {
  var sb = $id('sidebar');
  var scroll_bar_width = sb.offsetWidth - sb.clientWidth;
  if (scroll_bar_width > 0) {
    sb.style.paddingRight = scroll_bar_width + 'px';
  }

  sb.onmouseout = function () {
    this.style.paddingRight = 0;
  };
}

/**
 * Sync sidebar state from the sidebar
 */
function set_sidebar_toggle_state(should_be_open) {
  var is_open = document.body.className.indexOf('sidebar_open') !== -1;

  if (is_open !== should_be_open) {
    sidebar();
  }
}

/**
 * Collapses the sidebar
 */
function collapse_iframe_sidebar() {
  var iframe = $id('sidebar_iframe');

  if (!iframe) {
    return;
  }

  iframe.contentWindow.postMessage(
    JSON.stringify({type: 'collapse-sidebar'}),
    '*'
  );
}

function sidebar() {
  var bdy = document.body;

  if (!$id('sidebar')) {
    pull_sidebar();
  } else {
    if (bdy.className.indexOf('sidebar_open') == -1) {
      if ($id('sidebar').getAttribute('loaded') != 1) {
        sidebar_load_details();
      }

      bdy.className += ' sidebar_open';
      localStorage.setItem('sidebar_open', 'true');
    } else {
      bdy.className = trim(bdy.className.replace(/sidebar_open/g, ''));
      $id('sidebar').style.paddingRight = 0;
      localStorage.setItem('sidebar_open', 'false');
    }

    sidebar_cleanup();
    setTimeout(function () {
      sidebar_cleanup('final');
    }, 1000); //animation takes 1s to complete. Run after to cleanup anything if necessary
  }
}

function sidebar_scroll() {
  if ((ele = $id('sidebar'))) {
    ele.scrollTop = localStorage.getItem('sidebar_scrolltop');
    ele.onscroll = function () {
      localStorage.setItem('sidebar_scrolltop', this.scrollTop);
    };
  }
}

function sidebar_load_details() {
  if ((ele = $id('sidebar'))) {
    ele.setAttribute('loaded', 1);
  }

  sidebar_project_names();
}

function sidebar_project_names() {
  if ($id('sidebar_projects')) {
    var names = $id('sidebar_projects').getElementsByTagName('SPAN');
    var char_width = 7;
    for (var n = 0; n < names.length; n++) {
      var default_name = names[n].firstChild.nodeValue;
      var diff = names[n].scrollWidth - names[n].offsetWidth;
      if (diff > 0) {
        var len = default_name.length;
        var half = Math.round((len / 5) * 3);
        var part1 = default_name.substring(0, half);
        var part2 = default_name.substring(half);
        names[n].setAttribute('title', names[n].firstChild.nodeValue);

        var trim_letters = Math.ceil((diff / char_width) * 0.5);
        if (trim_letters > 0) {
          while (diff > 0) {
            part1 = rtrim(part1.substring(0, part1.length - trim_letters));
            part2 = ltrim(part2.substring(trim_letters));

            trim_letters = 2;
            names[n].firstChild.nodeValue = part1 + '...' + part2;
            diff = names[n].scrollWidth - names[n].offsetWidth;
          }
        }
      }
    }
  }
}

function sidebar_cleanup(type) {
  type = type || '';
  //UPDATE SCROLL IN GANTT & RESOURCE VIEW
  if (typeof match_scrolls == 'function') {
    //GANTT SCROLL
    set_scroll_bar();

    //RESOURCE VIEW
    if (
      $id('resource_view') &&
      $id('resource_view').className != 'resource_collapsed'
    ) {
      var left = $id('resource_view_list').offsetWidth;
      left += sidebar_width();

      $id('resource_view').style.left = left + 'px'; //RESOURCE VIEW
      set_resource_view_scroll(); //RESOURCE SCROLL
    }

    set_arrows(); //TASK ARROWS
  }

  //CALENDAR (WEEKLY VIEW)
  if (type == 'final' && typeof force_loop_tasks == 'function') {
    force_loop_tasks();
  }

  if (typeof match_scrolls == 'function') {
    move_scroll('negative');
    move_scroll('positive');
    setTimeout(match_scrolls, 100);
  }

  if (typeof set_position_time_sheet_today_message == 'function') {
    set_position_time_sheet_today_message();
  }
}

function save_sidebar_status(status) {
  var val = status == 'open' ? 'true' : 'false';
  localStorage.setItem('sidebar_open', val);
}

function sidebar_open_project(project_id, ele) {
  localStorage.setItem('sidebar_open', 'true');

  var dir = localStorage.getItem('project_dir') || 'schedule';
  if (ele) {
    dir = ele.getAttribute('dir');
  }

  window.location =
    '/' + $id('js_gantt_url').value + '/' + dir + '/?ids=' + project_id;
}

function sidebar_open_conversation(ele) {
  localStorage.setItem('sidebar_open', 'true');

  var target = ele.getAttribute('target');
  var target_id = ele.getAttribute('target_id');

  if ((ele = $id('conversation_' + target + '_' + target_id))) {
    ele.click();
  } else {
    localStorage.setItem('sidebar_open', 'true');
    window.location =
      '/' +
      $id('js_gantt_url').value +
      '/conversations/?ids=MY-ACTIVE&long_header=true&showall=all&onload=comment,' +
      target +
      ',' +
      target_id +
      ',comments';
  }
}

function pull_sidebar() {
  var ajaxRequest; // The variable that makes Ajax possible!

  try {
    // Opera 8.0+, Firefox, Safari
    ajaxRequest = new XMLHttpRequest();
  } catch (e) {
    // Internet Explorer Browsers
    try {
      ajaxRequest = new ActiveXObject('Msxml2.XMLHTTP');
    } catch (e) {
      try {
        ajaxRequest = new ActiveXObject('Microsoft.XMLHTTP');
      } catch (e) {
        // Something went wrong
        alert('Your browser broke!');
        return false;
      }
    }
  }

  // Create a function that will receive data sent from the server
  ajaxRequest.onreadystatechange = function () {
    if (ajaxRequest.readyState != 4) {
    } else if (ajaxRequest.readyState == 4 && ajaxRequest.status == 200) {
      var call_display = true;
      if ((sb = $id('sidebar'))) {
        sb.parentNode.removeChild(sb);
        call_display = false;
      }

      if ((bg = $id('sidebar_cover'))) {
        $id('sidebar_cover').click();
      }

      var div = $create('DIV');
      div.innerHTML = ajaxRequest.responseText;
      document.body.insertBefore(div, document.body.firstChild);

      if (call_display) {
        setTimeout(sidebar, 250);
      } else {
        sidebar_scroll();
      }
    } else {
    }
  };

  var queryString = null;
  ajaxRequest.open(
    'POST',
    '/' + $id('js_gantt_url').value + '/sidebar.php',
    true
  );
  ajaxRequest.setRequestHeader(
    'Content-type',
    'application/x-www-form-urlencoded'
  );
  ajaxRequest.send(queryString);
}

function sidebar_project_check(ele) {
  var parent = ele.parentNode.parentNode;
  var input = $id('sidebar_project_ids');
  var array = input.value.split(',');

  if (ele.checked) {
    parent.className += ' checked';
    array.push(ele.value);
  } else {
    parent.className = trim(parent.className.replace(/checked/g, ''));
    var key = js_in_array(ele.value, array);
    array[key] = '';
  }

  var temp = [];
  for (var i = 0; i < array.length; i++) {
    if (array[i] != '') {
      temp.push(array[i]);
    }
  }

  input.value = temp.join(',');
}

function sidebar_select_multiple_projects() {
  if ((ele = $id('sidebar_projects'))) {
    ele.className = trim(ele.className + ' select_projects');
  }
}

function sidebar_open_multiple_projects() {
  var ids = $id('sidebar_project_ids').value;
  var dir = 'schedule';
  var spans = $id('sidebar_projects').getElementsByTagName('SPAN');
  for (var s = 0; s < spans.length; s++) {
    if (spans[s].getAttribute('dir') != undefined) {
      dir = spans[s].getAttribute('dir');
      s = spans.length * 2;
      break;
    }
  }

  if (ids != '') {
    window.location =
      '/' + $id('js_gantt_url').value + '/' + dir + '/?ids=' + ids;
  }
}
/* END SIDEBAR */

/* OPEN PROJECT */
function set_project_url(ele) {
  var href = ele.getAttribute('href');
  var dir = localStorage.getItem('project_dir') || 'schedule';
  if (href.indexOf('_dir_') > -1) {
    href = href.replace('_dir_', dir);
  }
  ele.setAttribute('href', href);
}

/* BACKGROUND COVER */
function build_background_cover() {
  var div = $create('DIV');
  div.className = 'background_cover';
  document.body.appendChild(div);

  show_backdrop();
  return div;
}

function remove_background_cover(close_div) {
  var divs = document.body.getElementsByTagName('DIV');
  for (var d = 0; d < divs.length; d++) {
    if (divs[d].className == 'background_cover') {
      divs[d].parentNode.removeChild(divs[d]);
    }
  }

  if (close_div != '' && $id(close_div)) {
    $id(close_div).className += ' hidden';
  }
}

/* HEADER STUFF */
function update_tab_count(span, difference) {
  return;
}

function open_user_icon_details() {
  $id('header_user_icon_details').className = 'dropdown_standard';

  if ($id('header_background_cover') == undefined) {
    var div = build_background_cover();
    div.id = 'header_background_cover';
    div.style.background = 'none';
    div.onclick = function () {
      close_user_icon_details();
    };

    $id('header_user_icon').parentNode.className = 'active';
  }

  fetch_bookmarks();
}

function close_user_icon_details() {
  $id('header_background_cover').remove();
  $id('header_user_icon_details').className = 'hidden';
  $id('header_user_icon').parentNode.className = '';
}

function fetch_bookmarks() {
  new $ajax({
    parent: this,
    type: 'GET',
    url: API_URL + 'v1/bookmarks',
    response: function (data) {
      var json = json_decode(data.responseText);
      var parent = $id('bookmark_list');
      remove_child_nodes(parent);
      for (var i = 0; i < json.length; i++) {
        var div = $create('DIV');
        parent.appendChild(div);

        var del = $create('SPAN');
        del.appendChild($text('x'));
        del.setAttribute('bookmark_id', json[i].id);
        del.onclick = function () {
          delete_user_bookmark(this.getAttribute('bookmark_id'));
        };
        div.appendChild(del);

        var alink = $create('A');
        alink.className = 'blue';
        alink.href = json[i].url;

        alink.onclick = function () {
          event.preventDefault();
          navigate_window(this.getAttribute('href'));
        };

        alink.appendChild($text(json[i].name));
        div.appendChild(alink);
      }
    },
  });
}

function delete_user_bookmark(id) {
  var conf = custom_confirm('Are you sure you want to delete this bookmark?');
  conf['yes'].onclick = function () {
    new $ajax({
      parent: this,
      type: 'DELETE',
      url: API_URL + 'v1/bookmarks/' + id,
      response: function () {
        fetch_bookmarks();
      },
    });

    this.ondblclick();
  };
}

function open_user_help_details() {
  //CLEANUP FROM TOOLTIPS IF NEEDED
  if (typeof _show_tooltips != 'undefined') {
    if (_tooltip_step == 'help_docs' && _tooltip_div != null) {
      close_tooltip('help_docs');
      load_next_tooltip();
    }
  }

  $id('header_help_details').className = 'dropdown_standard';
  $id('support_help').parentNode.className = 'active';

  var div = build_background_cover();
  div.style.background = 'none';
  div.onclick = function () {
    $id('header_help_details').className = 'hidden';
    this.parentNode.removeChild(this);
    $id('support_help').parentNode.className = '';
  };
}

function select_header_tab(ele) {
  if (
    $id('background_cover') &&
    $id('background_cover').className != 'hidden'
  ) {
    $id('background_cover').click();
  }

  var header_tabs = $id('header_tabs');
  if (header_tabs) {
    var children = header_tabs.childNodes;
    for (var i = 0; i < children.length; i++) {
      var child = children[i];
      if (
        child.id != 'header_more_dropdown' &&
        !/header_tabs__go-premium-button/.test(child.className)
      ) {
        children[i].className = '';
      }
    }

    ele.className = 'selected';
  }
}

//HEADER CHECK CHECKBOX
function manage_check(ele, input) {
  var checkbox = input != null ? $id(input) : input;

  if (ele.className.indexOf('checked') > -1) {
    ele.className = ele.className.replace(/checked/g, '');

    if (input != null) {
      checkbox.checked = false;
    }
  } else {
    ele.className += ' checked';

    if (input != null) {
      checkbox.checked = true;
    }
  }
}

//OPEN DROPDOWN
function open_dd(which, direction) {
  var li = '';
  var dd = '';
  var icon = '';
  var default_behavior = true;

  if (which == 'schedule_menu') {
    icon = $id('schedule_menu');
    dd = $id('menu_dd_box');

    //LOAD BASELINES
    baseline_list();
    load_involved();
  } else if (which == 'view_menu') {
    icon = $id('view_menu');
    dd = $id('view_dd_box');

    if ($id('details_column_view_checkboxes')) {
      $id('details_column_view_checkboxes_parent').appendChild(
        $id('details_column_view_checkboxes')
      );
    }
  } else if (which == 'filter_resources') {
    icon = $id('filter_resources');
    dd = $id('filter_resources_dd_box');
  } else if (which == 'filter_dates') {
    icon = $id('filter_dates_other');
    dd = $id('date_filters_dd_box');
  } else if (which == 'zoom') {
    icon = $id('zoom_dd');
    dd = $id('zoom_dd_list');

    $id('zoom_interior').appendChild($id('zoom_picker'));
  } else if (which == 'color_dd') {
    icon = $id('color_picker_dd');
    dd = $id('color_picker_dd_list');
  } else if (which == 'resource_view') {
    icon = $id('resource_view_which');
    dd = $id('resource_view_which_options');
    default_behavior = false;
  } else if (which == 'filter_colors') {
    icon = $id('filter_colors');
    dd = $id('color_filters_dd_box');
  } else if (which == 'resource_view_format') {
    icon = $id('resource_view_format_dd');
    dd = $id('resource_view_format_dd_box');
  } else if (which == 'people_filter') {
    icon = $id('people_filter');
    dd = $id('people_filter_dropdown');

    setTimeout(function () {
      $id('people_search').focus();
    }, 200);
  } else if (which == 'projects_filter') {
    icon = $id('projects_filter');
    dd = $id('projects_filter_dropdown');

    setTimeout(function () {
      $id('project_search').focus();
    }, 200);
  } else if (which === 'share_menu') {
    icon = $id('invite_button');
    dd = $id('share_menu_dd');
  } else {
    if ($id(which) && $id(which + '_dropdown')) {
      icon = $id(which);
      dd = $id(which + '_dropdown');
    }
  }

  if (icon != '' && dd != '') {
    if (direction == 'open' && dd.className.indexOf('box_option') > -1) {
      direction = 'close';
    }

    if (direction == 'open') {
      close_previous_dds();
      clear_text();
      setTimeout(clear_text, 100);

      if (direction == 'open') {
        dd.setAttribute('open', true);

        if (default_behavior) {
          dd.className = 'box_option';

          //POSITION
          var position = real_position(icon);
          var left = position.x;
          left += sidebar_width();
          var top = position.y;
          top -= get_scrolltop();

          var page_height = page_sizes()[1] - 60;
          var page_width = page_sizes()[0];

          //if div will overflow out of the page
          var overflow = left * 1 + dd.offsetWidth - page_width;
          if (overflow > 0) {
            left -= overflow + 35;
          }

          dd.style.maxHeight =
            Math.round(((page_height - top) * 75) / 100) + 'px';
          dd.style.left = Math.round(left) + 'px';
          dd.style.top = Math.round(top) + 'px';
        } else {
          dd.className = '';
        }

        //FUNCTION CONTROLS
        dd.onmouseleave = function (event) {
          /**
           * Changing the selected options triggers a
           * network request which causes a fullscreen loader to
           * temporarily steal mouse events.
           * This check avoids closing the dropdown when in that case
           */
          if (event.relatedTarget.id === 'loader') {
            return;
          }
          this.setAttribute('mouse_over', 0);
          check_close(this, null);
        };
        dd.onmouseenter = function () {
          this.setAttribute('mouse_over', 1);
        };

        icon.setAttribute('child', dd.id);
        icon.onmouseenter = function () {
          $id(this.getAttribute('child')).setAttribute('mouse_over', 1);
        };
        icon.onmouseleave = function () {
          $id(this.getAttribute('child')).setAttribute('mouse_over', 0);
          check_close($id(this.getAttribute('child')), null);
        };
      }
    } else {
      close_previous_dds();
      clear_text();
      setTimeout(clear_text, 100);
    }
  }

  check_scroll();
}

function close_previous_dds() {
  //CLOSE ALL PREVIOUS OPENED DDs
  var divs = $id('open_dd_box').childNodes;
  for (var d = 0; d < divs.length; d++) {
    if (divs[d].tagName == 'DIV') {
      divs[d].className = 'hidden';
    }
  }
}

function check_close(dd, run) {
  if (run == null) {
    setTimeout(function () {
      check_close(dd, 1);
    }, 400);
  } else if (run != 1) {
    setTimeout(function () {
      check_close(dd, 1);
    }, 100);
  } else if (run == 1) {
    var select_open = document.activeElement.tagName == 'SELECT';
    if (dd.getAttribute('mouse_over') == 0 && !select_open) {
      dd.className = 'hidden';
      allow_hover = true;

      // notify callback event when closed
      on_dd_closed(dd.id);

      if (dd.getAttribute('target')) {
        $id(dd.getAttribute('target')).className = $id(
          dd.getAttribute('target')
        ).className.replace(/selected/g, '');
        $id(dd.getAttribute('target')).className = $id(
          dd.getAttribute('target')
        ).className.replace(/active/g, '');
      } else {
        document.body.style.overflowY = 'auto';
      }
    }
  }
}

// used to prevent duplicate callbacks being fired
var dd_closed_map = {};

function on_dd_closed(id) {
  if (!dd_closed_map[id]) {
    dd_closed_map[id] = true;

    switch (id) {
      case 'projects_list':
        load_selected_projects();
    }

    setTimeout(function () {
      delete dd_closed_map[id];
    }, 500);
  }
}

function initiate_search(ele) {
  ele.onfocus = null;
  ele.onkeyup = function (event) {
    if (event && event.keyCode == _master_keys['enter']) {
      var div = this.parentNode.parentNode;
      var eles = div.getElementsByTagName('DIV');
      for (var i = 0; i < eles.length; i++) {
        if (
          eles[i].getAttribute('searchable') == 'true' &&
          eles[i].className.indexOf('hidden') == -1
        ) {
          eles[i].getElementsByTagName('INPUT')[0].click();
          i = eles.length * 1;

          //CLEAR & UPDATE
          this.value = '';
          header_dd_filter_search(this, ele.id);
        }
      }
    } else {
      header_dd_filter_search(this, ele.id);
    }
  };
  ele.onmouseup = function () {
    this.select();
  };
}

function header_dd_filter_search(type, which) {
  if (which == 'people_search') {
    var opts = $id('people_filter_dropdown').getElementsByTagName('DIV');
  } else if (which == 'project_search') {
    var opts = $id('projects_filter_dropdown').getElementsByTagName('DIV');
  }

  if (opts) {
    var query = type.value;
    var is_highlight = false;
    for (var i = 0; i < opts.length; i++) {
      if (opts[i].getAttribute('searchable') == 'true') {
        //CLEAR HIGHLIGHT
        opts[i].className = trim(opts[i].className.replace(/highlight/g, ''));

        //SHOW OR HIDE
        if (
          query == '' ||
          opts[i].textContent
            .toLowerCase()
            .replace(/ /g, '')
            .indexOf(query.toLowerCase().replace(/ /g, '')) > -1
        ) {
          opts[i].className = trim(opts[i].className.replace(/hidden/g, ''));

          if (is_highlight == false && query != '') {
            opts[i].className += ' highlight';
            is_highlight = true;
          }
        } else {
          opts[i].className += ' hidden';
        }
      }
    }
  }
}

/* AUTO HEIGHT OF TEXTAREA */
function textarea_height(ele) {
  var new_height = ele.offsetHeight * 1 + 20;

  if (ele.offsetHeight < ele.scrollHeight) {
    ele.style.height = ele.scrollHeight * 1 + 20 + 'px';
  }

  if (ele.id == 'add_comment') {
    var type = '';
    if (_popup_key != '') {
      type = 'meta';
    } else if (_edit_key != '') {
      type = 'window';
    }

    if (type != '') {
      var parent =
        type == 'meta' ? $id('meta_target') : $id(_edit_key + '_edit_scroll');
      if (parent) {
        var additional_height = 70;
        additional_height += $id('comment_send_email_alert').offsetHeight * 1;
        additional_height += $id('comment_send_button').offsetHeight * 1;

        var height = parent.offsetHeight;
        ele.style.maxHeight = height - additional_height + 'px';

        //parent.scrollTop = ele.parentNode.parentNode.offsetTop;
      }
    }
  } else if (ele.getAttribute('message_type') == 'note') {
    var type = '';
    if (_popup_key != '') {
      type = 'meta';
    } else if (_edit_key != '') {
      type = 'window';
    }

    if (type != '') {
      var parent =
        type == 'meta' ? $id('meta_target') : $id(_edit_key + '_edit_scroll');
      if (parent) {
        var additional_height = 140;

        var height = parent.offsetHeight;
        ele.style.maxHeight = height - additional_height + 'px';

        //parent.scrollTop = ele.parentNode.parentNode.parentNode.offsetTop - 50;
      }
    }
  }
}

function free_text_html(text) {
  var t = text;
  t = t.replace(/</g, '&lt;');
  t = t.replace(/>/g, '&gt;');
  t = t.replace(/\n/g, '<br />\n');

  return linkify(t);
}
/* END TEXTAREA */

//MAKE INPUT TEXT A NUMBER
function make_numeric(input) {
  var input = input.replace(/,/g, '.');
  var string = new String(input);
  string = string.replace(/[^0-9.]/g, '');

  return string;
}

/* TEXT SELECTION */
function clear_text() {
  if (document.selection) document.selection.empty();
  else if (window.getSelection) window.getSelection().removeAllRanges();
}

function disable_selection(target) {
  disableSelection(target);
}

function enable_selection(target) {
  enableSelection(target);
}

/* INNER POPUP GANTT */
function open_inner_popup(ele) {
  close_inner_popup();

  //COVER
  var cover = build_background_cover();
  cover.onclick = function () {
    close_inner_popup();
  };
  cover.id = 'background_cover';
  if (ele.getAttribute('force_background') == 'true') {
    cover.className += ' force_background';
  }

  //CONTROLS
  var div = $create('DIV');
  div.id = 'inner_popup_options';
  document.body.appendChild(div);

  //CLOSE
  var close_option = $create('DIV');
  close_option.onclick = function () {
    close_inner_popup();
  };
  close_option.appendChild($text('Close (x)'));
  div.appendChild(close_option);

  //FULL SCREEN
  var full_screen = $create('DIV');
  full_screen.className = 'full_screen';
  var href = ele.getAttribute('href').replace('&public_keys=LOGIN', '');
  full_screen.setAttribute('href', href);
  full_screen.onclick = function () {
    if (window.location.toString().indexOf(this.getAttribute('href')) == -1) {
      navigate_window(this.getAttribute('href'));
    } else {
      navigate_window(this.getAttribute('href'));
      document.location.reload();
    }
  };
  full_screen.appendChild($text('Full Screen'));
  div.appendChild(full_screen);

  //IFRAME
  var iframe = $create('IFRAME');
  iframe.src = ele.getAttribute('href');
  iframe.id = 'inner_popup';
  document.body.appendChild(iframe);

  document.body.style.overflowY = 'hidden';
}

function close_inner_popup() {
  while ($id('inner_popup') != null) {
    $id('inner_popup').parentNode.removeChild($id('inner_popup'));
  }

  while ($id('inner_popup_options') != null) {
    $id('inner_popup_options').parentNode.removeChild(
      $id('inner_popup_options')
    );
  }

  while ($id('background_cover') != null) {
    $id('background_cover').parentNode.removeChild($id('background_cover'));
  }

  if ($id('resource_assign_close_button')) {
    $id('resource_assign_close_button').click();
  }

  document.body.style.overflowY = 'auto';

  //RELOAD GANTT
  if (typeof load_gantt == 'function') {
    load_gantt();
    $id('header_user_icon_details').className = 'hidden';
  }

  document.body.style.overflowY = 'auto';
}
/* END INNER POPUP GANTT */

/* ADJUST TEXT FOR AJAX */
function tweak_text_for_get(name_value) {
  if (name_value != undefined) {
    name_value = name_value.toString();
    name_value = name_value.replace(/&/g, '%26');
    name_value = name_value.replace(/#/g, '%23');
    name_value = name_value.replace(/&/g, '%2C');
    name_value = name_value.replace(/"/g, '%22');
    name_value = name_value.replace(/'/g, '%27');
    name_value = name_value.replace(/\+/g, '%2B');
    name_value = name_value.replace(/\@/g, '%40');
    name_value = name_value.replace(/\$/g, '%24');
    name_value = name_value.replace(/\^/g, '%5E');
    name_value = name_value.replace(/\(/g, '%28');
    name_value = name_value.replace(/\)/g, '%29');
    name_value = name_value.replace(/\`/g, '%60');
    name_value = name_value.replace(/\~/g, '%7E');
    name_value = name_value.replace(/\?/g, '%3F');
    name_value = name_value.replace(/\>/g, '%3E');
    name_value = name_value.replace(/\>/g, '%3C');
    name_value = name_value.replace(/\{/g, '%7B');
    name_value = name_value.replace(/\{/g, '%7B');
    name_value = name_value.replace(/\}/g, '%7D');
    name_value = name_value.replace(/\[/g, '%5B');
    name_value = name_value.replace(/\]/g, '%5D');
    name_value = name_value.replace(/\|/g, '%7C');

    return name_value;
  }
}
/* END ADJUST TEXT FOR AJAX */

/* TRIM STRING */
function trim(s) {
  return rtrim(ltrim(s));
}

function ltrim(s) {
  var l = 0;
  while (l < s.length && s[l] == ' ') {
    l++;
  }
  return s.substring(l, s.length);
}

function rtrim(s) {
  var r = s.length - 1;
  while (r > 0 && s[r] == ' ') {
    r -= 1;
  }
  return s.substring(0, r + 1);
}

function no_spaces(s) {
  s = s.replace(/ /g, '');
  return trim(s);
}
/* END TRIM STRING */

/* PAGE LISTENERS */
function addListener(element, type, expression, bubbling) {
  bubbling = bubbling || false;

  if (window.addEventListener) {
    // Standard
    element.addEventListener(type, expression, bubbling);
    return true;
  } else if (window.attachEvent) {
    // IE
    element.attachEvent('on' + type, expression);
    return true;
  } else return false;
}

function removeListener(element, type, expression, bubbling) {
  if (window.removeEventListener) {
    // Standard
    element.removeEventListener(type, expression, bubbling);
    return true;
  } else if (window.detachEvent) {
    // IE
    element.detachEvent('on' + type, expression);
    return true;
  } else return false;
}
/* END PAGE LISTENERS */

/* XML NODE VALUE */
function getNodeValue(parent, tagName) {
  var node = parent.getElementsByTagName(tagName)[0];
  return node && node.firstChild ? node.firstChild.nodeValue : '';
}
/* END XML NODE VALUE */

/* REMOVE CHILDREN */
function remove_child_nodes(parent) {
  if (parent && parent.hasChildNodes()) {
    while (parent.childNodes.length >= 1) {
      parent.removeChild(parent.firstChild);
    }
  }
}
/* REMOVE CHILDREN */

/* WINDOW SIZES */
function window_size(which) {
  var winW = 630,
    winH = 460;
  if (document.body && document.body.offsetWidth) {
    winW = document.body.offsetWidth;
    winH = document.body.offsetHeight;
  }
  if (
    document.compatMode == 'CSS1Compat' &&
    document.documentElement &&
    document.documentElement.offsetWidth
  ) {
    winW = document.documentElement.offsetWidth;
    winH = document.documentElement.offsetHeight;
  }
  if (window.innerWidth && window.innerHeight) {
    winW = window.innerWidth;
    winH = window.innerHeight;
  }

  if (which == 'height') {
    return winH;
  } else if (which == 'width') {
    return winW;
  } else {
    return [winW, winH];
  }
}

function page_sizes() {
  var myWidth = 0,
    myHeight = 0;
  if (typeof window.innerWidth == 'number') {
    //Non-IE
    myWidth = window.innerWidth;
    myHeight = window.innerHeight;
  } else if (
    document.documentElement &&
    (document.documentElement.clientWidth ||
      document.documentElement.clientHeight)
  ) {
    //IE 6+ in 'standards compliant mode'
    myWidth = document.documentElement.clientWidth;
    myHeight = document.documentElement.clientHeight;
  } else if (
    document.body &&
    (document.body.clientWidth || document.body.clientHeight)
  ) {
    //IE 4 compatible
    myWidth = document.body.clientWidth;
    myHeight = document.body.clientHeight;
  }

  return [myWidth, myHeight];
}
/* END WINDOW SIZES */

/* SCROLLS */
function get_scrolltop() {
  var scrOfY = 0;
  if (typeof window.pageYOffset == 'number') {
    //Netscape compliant
    scrOfY = window.pageYOffset;
  } else if (
    document.body &&
    (document.body.scrollLeft || document.body.scrollTop)
  ) {
    //DOM compliant
    scrOfY = document.body.scrollTop;
  } else if (
    document.documentElement &&
    (document.documentElement.scrollLeft || document.documentElement.scrollTop)
  ) {
    //IE6 standards compliant mode
    scrOfY = document.documentElement.scrollTop;
  }
  return scrOfY;
}

function get_scrollleft() {
  var scrOfX = 0;
  if (typeof window.pageYOffset == 'number') {
    //Netscape compliant
    scrOfX = window.pageXOffset;
  } else if (
    document.body &&
    (document.body.scrollLeft || document.body.scrollTop)
  ) {
    //DOM compliant
    scrOfX = document.body.scrollLeft;
  } else if (
    document.documentElement &&
    (document.documentElement.scrollLeft || document.documentElement.scrollTop)
  ) {
    //IE6 standards compliant mode
    scrOfX = document.documentElement.scrollLeft;
  }
  return scrOfX;
}
/* END SCROLLS */

/* POSITION */
function real_position(element) {
  var sidebar = sidebar_width() * -1;
  var rectObject = element.getBoundingClientRect();
  var top = rectObject.top * 1;
  top += element.offsetHeight * 1;
  top += get_scrolltop() * 1;

  var left = rectObject.left + sidebar; // (1) finds position relative do the page edge. (2) remove sidebar width to find width relative to the body's left edge

  return {x: left, y: top};
}
/* END POSITION */

/* IN ARRAY */
function js_in_array(needle, haystack) {
  var key = -1;
  for (i = 0; i < haystack.length; i++) {
    if (haystack[i] == needle) {
      key = i;
    }
  }
  return key;
}

function js_in_unorganized_array(needle, haystack) {
  var key = false;
  for (var k in haystack) {
    if (haystack[k] == needle) {
      key = k;
    }
  }
  return key;
}
/* END IN ARRAY */

/* TRUE OFFSET TOP */
function true_offset_top(obj) {
  var curleft = (curtop = 0);

  if (obj.offsetParent) {
    do {
      curleft += obj.offsetLeft;
      curtop += obj.offsetTop;
    } while ((obj = obj.offsetParent));
  }

  //return [curleft,curtop];
  return curtop;
}
/* END TRUE OFFSET TOP */

function hide_backdrop() {
  if (get_is_embedded_view()) {
    parent_post_message('hide-backdrop');
  }

  const htmlCollection = document.getElementsByClassName('background_cover')
  const bg = htmlCollection[htmlCollection.length-1]; // only hide top backdrop if multiple

  if (!bg) {
    return;
  }

  document.body.removeChild(bg);
}

function show_backdrop() {
  if (get_is_embedded_view()) {
    parent_post_message('show-backdrop');
  }
}

function click_current_backdrop() {
  var backdrop = document.getElementsByClassName('background_cover')[0];

  if (backdrop && backdrop.onclick) {
    backdrop.onclick();
  }
}

/* ALERT / CONFIRM */
function custom_alert(message, buttons) {
  buttons = typeof buttons !== 'undefined' ? buttons : true;
  ///message = message.replace(/</g,"&lt;");

  var bg = build_background_cover();
  bg.id = 'custom_alert_cover';
  bg.style.cursor = 'default';
  bring_to_front(bg);

  var interior = $create('DIV');
  interior.id = 'custom_alert_message';
  bg.appendChild(interior);

  var message_div = $create('DIV');
  message_div.className = 'message';
  message_div.innerHTML = message;
  interior.appendChild(message_div);

  if (buttons) {
    var okay = $create('DIV');
    okay.className = 'okay';
    okay.ondblclick = hide_backdrop;
    okay.onclick = hide_backdrop;
    okay.appendChild($text('Ok'));
    interior.appendChild(okay);

    return okay;
  } else {
    var closer = $create('DIV');
    closer.className = 'closer';
    closer.appendChild(document.createTextNode('X'));
    closer.onclick = hide_backdrop;
    interior.appendChild(closer);

    //ALLOW BACKGROUND TO CLOSE
    interior.onclick = function (event) {
      var e = event || window.event;

      //IE9 & Other Browsers
      if (e.stopPropagation) {
        e.stopPropagation();
      }
      //IE8 and Lower
      else {
        e.cancelBubble = true;
      }
    };
    bg.onclick = hide_backdrop;

    message_div.style.paddingBottom = 0;

    return interior;
  }
}

function custom_confirm(message) {
  var bg = build_background_cover();
  bg.id = 'custom_alert_cover';
  bg.style.cursor = 'default';
  bring_to_front(bg);

  var interior = $create('DIV');
  interior.id = 'custom_alert_message';
  bg.appendChild(interior);

  var message_div = $create('DIV');
  message_div.className = 'message';
  message_div.innerHTML = message;
  interior.appendChild(message_div);

  var buttons_wrapper = $create('DIV');
  buttons_wrapper.className = 'buttons_wrapper';

  var no = $create('DIV');
  no.id = 'custom_alert_no';
  no.className = 'okay no';
  no.ondblclick = hide_backdrop;
  no.onclick = hide_backdrop;
  no.appendChild($text('No'));
  buttons_wrapper.appendChild(no);

  var yes = $create('DIV');
  yes.id = 'custom_alert_yes';
  yes.className = 'okay';
  yes.ondblclick = hide_backdrop;
  yes.appendChild($text('Yes'));
  buttons_wrapper.appendChild(yes);
  interior.appendChild(buttons_wrapper);

  var ret = [];
  ret['yes'] = yes;
  ret['no'] = no;
  ret['ele'] = bg;
  ret['div'] = message_div;

  return ret;
}

function api_setup(url) {
  window_opener(url, 720, 550);
}

function window_opener(url, wdth, hght) {
  var wdth = wdth.toString();
  var hght = hght.toString();

  //RESOLUTION
  var resx = screen.width;
  var resy = screen.height;

  if (wdth.indexOf('%') > -1) {
    var strip_width = wdth.replace(/%/g, '');
    var wdth = Math.ceil((resx * strip_width) / 100);
  } else {
    var wdth = wdth * 1;
  }

  if (hght.indexOf('%') > -1) {
    var strip_width = hght.replace(/%/g, '');
    var hght = Math.ceil((resy * strip_width) / 100);
  } else {
    var hght = hght * 1;
  }

  //LEFT AND TOP POSITIONING
  var lft = resx * 0.5 - wdth * 0.5 > 0 ? resx * 0.5 - wdth * 0.5 : 0;
  var tp = resy * 0.5 - hght * 0.5 > 0 ? resy * 0.5 - hght * 0.5 : 0;

  var nm = '';

  while (nm.length < 10) {
    nm += Math.round(Math.random() * 10);
  }

  window_name = 'window_' + nm;
  var win = window.open(
    url,
    window_name,
    'scrollbars=yes,menubar=no,height=' +
      hght +
      ',width=' +
      wdth +
      ',left=' +
      lft +
      ',top=' +
      tp +
      ',resizable=yes,toolbar=no,location=no,status=no'
  );
  //win.moveTo(lft, tp);

  return win;
}

function day_of_the_week(string) {
  var days = ['Sun', 'Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat'];
  string = string.replace(/-/g, '/');
  var check = new Date(dateFormat(string, 'default'));

  return days[check.getDay()];
}

function to_two(string) {
  return string * 1 < 10 ? '0' + string * 1 : string;
}

function next_day(date, increment) {
  increment = increment || 1;
  if (increment == 0) {
    return date;
  } else {
    var dt = new Date(date + 'T12:00:00Z');
    var y = dt.getFullYear();
    var m = to_two(dt.getMonth() * 1);
    var d = to_two(dt.getDate() * 1 + increment);

    var ret_date = new Date(y, m, d);
    var y = ret_date.getFullYear();
    var m = to_two(ret_date.getMonth() * 1 + 1);
    var d = to_two(ret_date.getDate());
    var ret = y + '-' + m + '-' + d;

    return ret;
  }
}

function pretty_time(string) {
  string = string.replace(/-/g, '/');
  string = dateFormat(string, 'h:MM tt');
  return string;
}

var tg_date_check = [
  'Sunday',
  'Monday',
  'Tuesday',
  'Wednesday',
  'Thursday',
  'Friday',
  'Saturday',
];

function pretty_day(date) {
  return tg_date_check[date.getDay()];
}

function pretty_date(string, word_days, force_format) {
  word_days = word_days || 'yes';
  force_format = force_format || _date_format;

  if (string == '' || string == '0000-00-00') {
    return '';
  } else if (typeof dateFormat == 'undefined') {
    return string;
  } else if (_date_format != undefined) {
    if (typeof day_diff == 'function') {
      //SEE IF IT SHOULD BE TOMORROW, ETC
      var today = new Date();
      var t_day =
        today.getFullYear() +
        '-' +
        to_two(today.getMonth() * 1 + 1) +
        '-' +
        today.getDate();

      var diff = day_diff(t_day, string, [0, 1, 2, 3, 4, 5, 6], [], true);
      if (diff != 0) {
        diff = diff > 0 ? diff * 1 - 1 : diff;
        diff = diff < 0 ? diff * 1 + 1 : diff;
      }

      if (diff == 0 && word_days == 'yes') {
        return 'Today';
      } else if (diff == 1 && word_days == 'yes') {
        return 'Tomorrow';
      } else if (diff == -1 && word_days == 'yes') {
        return 'Yesterday';
      } else if (diff > 1 && diff < 7 && word_days == 'yes') {
        string = string.replace(/-/g, '/');
        var check = new Date(dateFormat(string, 'default'));
        return pretty_day(check);
      } else {
        string = string.replace(/-/g, '/');
        string = dateFormat(string, force_format);

        return string;
      }
    } else {
      string = string.replace(/-/g, '/');
      string = dateFormat(string, force_format);

      return string;
    }
  }
}

function day_diff(start, end, project_days, holidays, count_today) {
  if (start != '' && end != '') {
    var go_negative = false;

    var start_split = start.split('-');
    start_split[2] = start_split[2] * 1;
    var end_split = end.split('-');
    end_split[2] = end_split[2] * 1;

    var start_date = new Date(
      start_split[0],
      start_split[1] - 1,
      start_split[2]
    );
    var end_date = new Date(end_split[0], end_split[1] - 1, end_split[2]);

    //IF START IS AFTER END DATE
    if (start_date > end_date) {
      var start_date = new Date(end_split[0], end_split[1] - 1, end_split[2]);
      var end_date = new Date(
        start_split[0],
        start_split[1] - 1,
        start_split[2]
      );

      start_split[0] = end_split[0];
      start_split[1] = end_split[1] * 1;
      start_split[2] = end_split[2];

      go_negative = true;
    }

    var counter = 0;
    var day_count = count_today ? 1 : 0;
    while (start_date < end_date) {
      counter++;
      start_date = new Date(
        start_split[0],
        start_split[1] - 1,
        start_split[2] + counter
      );

      //MAKE SURE IT FALLS ON A VALID DAY
      if (
        project_days.length == 7 ||
        js_in_array(start_date.getDay(), project_days) > -1
      ) {
        //MAKE SURE IT DOES NOT FALL ON A HOLIDAY
        if (holidays.length == 0) {
          //IF NO HOLIDAYS - SKIP AND COUNT
          day_count++;
        } else {
          //IF HAS HOLIDAYS - MAKE SURE IT's NOT A HOLIDAY
          var rdate =
            '-' + (start_date.getMonth() * 1 + 1) + '-' + start_date.getDate();
          var real_date = start_date.getFullYear() + rdate;
          var star_date = '*' + rdate;

          if (
            js_in_array(real_date, holidays) == -1 &&
            js_in_array(star_date, holidays) == -1
          ) {
            day_count++;
          }
        }
      }
    }

    return go_negative == false ? day_count : day_count * 1 * -1;
  } else {
    return 0;
  }
}

/*
 * Date Format 1.2.3
 * (c) 2007-2009 Steven Levithan <stevenlevithan.com>
 * MIT license
 *
 * Includes enhancements by Scott Trenda <scott.trenda.net>
 * and Kris Kowal <cixar.com/~kris.kowal/>
 *
 * Accepts a date, a mask, or a date and a mask.
 * Returns a formatted version of the given date.
 * The date defaults to the current date/time.
 * The mask defaults to dateFormat.masks.default.
 */

var dateFormat = (function () {
  var token = /d{1,4}|m{1,4}|yy(?:yy)?|([HhMsTt])\1?|[LloSZ]|"[^"]*"|'[^']*'/g,
    timezone =
      /\b(?:[PMCEA][SDP]T|(?:Pacific|Mountain|Central|Eastern|Atlantic) (?:Standard|Daylight|Prevailing) Time|(?:GMT|UTC)(?:[-+]\d{4})?)\b/g,
    timezoneClip = /[^-+\dA-Z]/g,
    pad = function (val, len) {
      val = String(val);
      len = len || 2;
      while (val.length < len) val = '0' + val;
      return val;
    };

  // Regexes and supporting functions are cached through closure
  return function (date, mask, utc) {
    var dF = dateFormat;

    // You can't provide utc if you skip other args (use the "UTC:" mask prefix)
    if (
      arguments.length == 1 &&
      Object.prototype.toString.call(date) == '[object String]' &&
      !/\d/.test(date)
    ) {
      mask = date;
      date = undefined;
    }

    // Passing date through Date applies Date.parse, if necessary
    date = date ? new Date(date) : new Date();
    if (isNaN(date)) throw SyntaxError('invalid date');

    mask = String(dF.masks[mask] || mask || dF.masks['default']);

    // Allow setting the utc argument via the mask
    if (mask.slice(0, 4) == 'UTC:') {
      mask = mask.slice(4);
      utc = true;
    }

    var _ = utc ? 'getUTC' : 'get',
      d = date[_ + 'Date'](),
      D = date[_ + 'Day'](),
      m = date[_ + 'Month'](),
      y = date[_ + 'FullYear'](),
      H = date[_ + 'Hours'](),
      M = date[_ + 'Minutes'](),
      s = date[_ + 'Seconds'](),
      L = date[_ + 'Milliseconds'](),
      o = utc ? 0 : date.getTimezoneOffset(),
      flags = {
        d: d,
        dd: pad(d),
        ddd: dF.i18n.dayNames[D],
        dddd: dF.i18n.dayNames[D + 7],
        m: m + 1,
        mm: pad(m + 1),
        mmm: dF.i18n.monthNames[m],
        mmmm: dF.i18n.monthNames[m + 12],
        yy: String(y).slice(2),
        yyyy: y,
        h: H % 12 || 12,
        hh: pad(H % 12 || 12),
        H: H,
        HH: pad(H),
        M: M,
        MM: pad(M),
        s: s,
        ss: pad(s),
        l: pad(L, 3),
        L: pad(L > 99 ? Math.round(L / 10) : L),
        t: H < 12 ? 'a' : 'p',
        tt: H < 12 ? 'am' : 'pm',
        T: H < 12 ? 'A' : 'P',
        TT: H < 12 ? 'AM' : 'PM',
        Z: utc
          ? 'UTC'
          : (String(date).match(timezone) || [''])
              .pop()
              .replace(timezoneClip, ''),
        o:
          (o > 0 ? '-' : '+') +
          pad(Math.floor(Math.abs(o) / 60) * 100 + (Math.abs(o) % 60), 4),
        S: ['th', 'st', 'nd', 'rd'][
          d % 10 > 3 ? 0 : (((d % 100) - (d % 10) != 10) * d) % 10
        ],
      };

    return mask.replace(token, function ($0) {
      return $0 in flags ? flags[$0] : $0.slice(1, $0.length - 1);
    });
  };
})();

// Some common format strings
dateFormat.masks = {
  default: 'ddd mmm dd yyyy HH:MM:ss',
  shortDate: 'm/d/yy',
  mediumDate: 'mmm d, yyyy',
  longDate: 'mmmm d, yyyy',
  fullDate: 'dddd, mmmm d, yyyy',
  shortTime: 'h:MM TT',
  mediumTime: 'h:MM:ss TT',
  longTime: 'h:MM:ss TT Z',
  isoDate: 'yyyy-mm-dd',
  isoTime: 'HH:MM:ss',
  isoDateTime: "yyyy-mm-dd'T'HH:MM:ss",
  isoUtcDateTime: "UTC:yyyy-mm-dd'T'HH:MM:ss'Z'",
};

// Internationalization strings
dateFormat.i18n = {
  dayNames: [
    'Sun',
    'Mon',
    'Tue',
    'Wed',
    'Thu',
    'Fri',
    'Sat',
    'Sunday',
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
  ],
  monthNames: [
    'Jan',
    'Feb',
    'Mar',
    'Apr',
    'May',
    'Jun',
    'Jul',
    'Aug',
    'Sep',
    'Oct',
    'Nov',
    'Dec',
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December',
  ],
};

// For convenience...
Date.prototype.format = function (mask, utc) {
  return dateFormat(this, mask, utc);
};

function time_difference(time1, time2) {
  var date1 = new Date(time1);
  var date2 = new Date(time2);

  var diff = date2.getTime() - date1.getTime();

  var msec = diff;
  var hh = Math.floor(msec / 1000 / 60 / 60);
  msec -= hh * 1000 * 60 * 60;
  var mm = Math.floor(msec / 1000 / 60);
  msec -= mm * 1000 * 60;
  var ss = Math.floor(msec / 1000);
  msec -= ss * 1000;

  var ret = '';
  ret += to_two(hh) + ':';
  ret += to_two(mm);
  //ret += ":" + to_two(ss);
  return ret;
}

/* KEYCODE STUFF */
var _master_keys = new Array();
_master_keys['escape'] = 27;
_master_keys['esc'] = 27;
_master_keys['enter'] = 13;
_master_keys['up'] = 38;
_master_keys['down'] = 40;
_master_keys['tab'] = 9;
_master_keys['shift'] = 16;
_master_keys['command'] = 91;
_master_keys['control'] = 17;
_master_keys['backspace'] = 8;
_master_keys['left_arrow'] = 37;
_master_keys['up_arrow'] = 38;
_master_keys['right_arrow'] = 39;
_master_keys['down_arrow'] = 40;

/* LOADING */
var _is_loading = null;
function start_load() {
  _is_loading = setTimeout(function () {
    display_loading();
  }, 1);
  addListener(document.body, 'mousemove', getMousePos, true);
}

function display_loading(is_not_blocking) {
  var loader = $id('loader');
  if (is_not_blocking === true) {
    loader.className = '';
  } else {
    loader.className = 'blocking';
  }
}

function finish_load() {
  clearTimeout(_is_loading);

  var loader = $id('loader');
  if (loader) {
    loader.className = 'hidden';
  }
}
/* END LOADING */

/* IFRAME */
function open_iframe(url, do_refresh) {
  do_refresh = do_refresh || 1;

  var cover = build_background_cover();
  cover.onclick = function () {
    close_iframe();
    hide_backdrop();
  };
  cover.id = 'iframe_cover';
  //cover.style.zIndex = "10000003";

  $id('iframe_wrapper').className = '';
  $id('project_iframe').src = url;
  $id('project_iframe').className = '';
  $id('project_iframe').setAttribute('do_refresh', do_refresh);

  //var open_resources = ($id("task_edit_resource_list").className != "hidden") ? "open_resources" : "";
  //$id("project_iframe").setAttribute("open_resources",open_resources);

  $id('tg_body').style.overflowY = 'hidden';
}

function close_iframe() {
  if ($id('iframe_cover')) {
    $id('iframe_cover').parentNode.removeChild($id('iframe_cover'));
  }

  if (
    false &&
    $id('project_iframe') &&
    $id('project_iframe').getAttribute('do_refresh') == 1
  ) {
    var win = '';
    var id = '';

    //SEE IF ANY WINDOWS ARE OPEN
    var edits = $id('edit_window');
    if (edits && edits.className != 'hidden') {
      win = edits.getAttribute('target');
      id = edits.getAttribute('target_id');
    }

    var open_resources = $id('project_iframe').getAttribute('open_resources');
    _reopen_badge = null;

    //IF A COMMENT WINDOW WAS OPENED
    if (
      $id('meta_popup') &&
      $id('meta_popup').className.indexOf('hidden') > -1
    ) {
      var which =
        $id('meta_left_tab').className.indexOf('comment') > -1
          ? 'comments'
          : 'documents';
      if (which == 'comments') {
        _reopen_badge = 'comments';
      }
    }

    //BUILD THE FUNCTION ARRAY
    var array =
      win != '' && id != '' ? ['load_edit', win, id, null, open_resources] : '';

    while ($id('background_cover') != null) {
      $id('background_cover').parentNode.removeChild($id('background_cover'));
    }

    if (_version == 'activity') {
      load_activity();
    } else {
      load_gantt(array);
    }
  }

  $id('project_iframe').src = '../schedule/blank.html';
  $id('iframe_wrapper').className = 'hidden';

  $id('tg_body').style.overflowY = 'auto';
}

function open_footer_share(direction, ele) {
  var target = $id('footer_share');

  if (direction == 'open' && target) {
    var background = build_background_cover();
    background.style.zIndex = '99999';
    background.style.background = 'none';
    background.onclick = function () {
      if ($id('footer_share')) {
        $id('footer_share').className = 'hidden';
      }

      this.parentNode.removeChild(this);
    };

    var left = ele.offsetLeft;
    target.className = '';
    target.style.left = left + 'px';
  } else if (target) {
    target.className = 'hidden';
  }
}

function open_intercom() {
  if ((d = $id('footer_intercom_button'))) {
    d.click();
  }

  return false;
}

/*!
 * linkify - v0.3 - 6/27/2009
 * http://benalman.com/code/test/js-linkify/
 *
 * Copyright (c) 2009 "Cowboy" Ben Alman
 * Licensed under the MIT license
 * http://benalman.com/about/license/
 *
 * Some regexps adapted from http://userscripts.org/scripts/review/7122
 */

// Turn text into linkified html.
//
// var html = linkify( text, options );
//
// options:
//
//  callback (Function) - default: undefined - if defined, this will be called
//    for each link- or non-link-chunk with two arguments, text and href. If the
//    chunk is non-link, href will be omitted.
//
//  punct_regexp (RegExp | Boolean) - a RegExp that can be used to trim trailing
//    punctuation from links, instead of the default.
//
// This is a work in progress, please let me know if (and how) it fails!

window.linkify = (function () {
  var SCHEME = '[a-z\\d.-]+://',
    IPV4 =
      '(?:(?:[0-9]|[1-9]\\d|1\\d{2}|2[0-4]\\d|25[0-5])\\.){3}(?:[0-9]|[1-9]\\d|1\\d{2}|2[0-4]\\d|25[0-5])',
    HOSTNAME = '(?:(?:[^\\s!@#$%^&*()_=+[\\]{}\\\\|;:\'",.<>/?]+)\\.)+',
    TLD =
      '(?:ac|ad|aero|ae|af|ag|ai|al|am|an|ao|aq|arpa|ar|asia|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|biz|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|cat|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|coop|com|co|cr|cu|cv|cx|cy|cz|de|dj|dk|dm|do|dz|ec|edu|ee|eg|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gov|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|info|int|in|io|iq|ir|is|it|je|jm|jobs|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mil|mk|ml|mm|mn|mobi|mo|mp|mq|mr|ms|mt|museum|mu|mv|mw|mx|my|mz|name|na|nc|net|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|org|pa|pe|pf|pg|ph|pk|pl|pm|pn|pro|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|sk|sl|sm|sn|so|sr|st|su|sv|sy|sz|tc|td|tel|tf|tg|th|tj|tk|tl|tm|tn|to|tp|travel|tr|tt|tv|tw|tz|ua|ug|uk|um|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|xn--0zwm56d|xn--11b5bs3a9aj6g|xn--80akhbyknj4f|xn--9t4b11yi5a|xn--deba0ad|xn--g6w251d|xn--hgbk6aj7f53bba|xn--hlcj6aya9esc7a|xn--jxalpdlp|xn--kgbechtv|xn--zckzah|ye|yt|yu|za|zm|zw)',
    HOST_OR_IP = '(?:' + HOSTNAME + TLD + '|' + IPV4 + ')',
    PATH = '(?:[;/][^#?<>\\s]*)?',
    QUERY_FRAG = '(?:\\?[^#<>\\s]*)?(?:#[^<>\\s]*)?',
    URI1 = '\\b' + SCHEME + '[^<>\\s]+',
    URI2 = '\\b' + HOST_OR_IP + PATH + QUERY_FRAG + '(?!\\w)',
    MAILTO = 'mailto:',
    EMAIL =
      '(?:' +
      MAILTO +
      ")?[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@" +
      HOST_OR_IP +
      QUERY_FRAG +
      '(?!\\w)',
    URI_RE = new RegExp('(?:' + URI1 + '|' + URI2 + '|' + EMAIL + ')', 'ig'),
    SCHEME_RE = new RegExp('^' + SCHEME, 'i'),
    quotes = {
      "'": '`',
      '>': '<',
      ')': '(',
      ']': '[',
      '}': '{',
      '»': '«',
      '›': '‹',
    },
    default_options = {
      callback: function (text, href) {
        return href
          ? '<a href="' +
              href +
              '" title="' +
              href +
              '" target="_blank">' +
              text +
              '</a>'
          : text;
      },
      punct_regexp:
        /(?:[!?.,:;'"]|(?:&|&amp;)(?:lt|gt|quot|apos|raquo|laquo|rsaquo|lsaquo);)$/,
    };

  return function (txt, options) {
    options = options || {};

    // Temp variables.
    var arr,
      i,
      link,
      href,
      // Output HTML.
      html = '',
      // Store text / link parts, in order, for re-combination.
      parts = [],
      // Used for keeping track of indices in the text.
      idx_prev,
      idx_last,
      idx,
      link_last,
      // Used for trimming trailing punctuation and quotes from links.
      matches_begin,
      matches_end,
      quote_begin,
      quote_end;

    // Initialize options.
    for (i in default_options) {
      if (options[i] === undefined) {
        options[i] = default_options[i];
      }
    }

    // Find links.
    while ((arr = URI_RE.exec(txt))) {
      link = arr[0];
      idx_last = URI_RE.lastIndex;
      idx = idx_last - link.length;

      // Not a link if preceded by certain characters.
      if (/[\/:]/.test(txt.charAt(idx - 1))) {
        continue;
      }

      // Trim trailing punctuation.
      do {
        // If no changes are made, we don't want to loop forever!
        link_last = link;

        quote_end = link.substr(-1);
        quote_begin = quotes[quote_end];

        // Ending quote character?
        if (quote_begin) {
          matches_begin = link.match(
            new RegExp('\\' + quote_begin + '(?!$)', 'g')
          );
          matches_end = link.match(new RegExp('\\' + quote_end, 'g'));

          // If quotes are unbalanced, remove trailing quote character.
          if (
            (matches_begin ? matches_begin.length : 0) <
            (matches_end ? matches_end.length : 0)
          ) {
            link = link.substr(0, link.length - 1);
            idx_last--;
          }
        }

        // Ending non-quote punctuation character?
        if (options.punct_regexp) {
          link = link.replace(options.punct_regexp, function (a) {
            idx_last -= a.length;
            return '';
          });
        }
      } while (link.length && link !== link_last);

      href = link;

      // Add appropriate protocol to naked links.
      if (!SCHEME_RE.test(href)) {
        href =
          (href.indexOf('@') !== -1
            ? !href.indexOf(MAILTO)
              ? ''
              : MAILTO
            : !href.indexOf('irc.')
            ? 'irc://'
            : !href.indexOf('ftp.')
            ? 'ftp://'
            : 'http://') + href;
      }

      // Push preceding non-link text onto the array.
      if (idx_prev != idx) {
        parts.push([txt.slice(idx_prev, idx)]);
        idx_prev = idx_last;
      }

      // Push massaged link onto the array
      parts.push([link, href]);
    }

    // Push remaining non-link text onto the array.
    parts.push([txt.substr(idx_prev)]);

    // Process the array items.
    for (i = 0; i < parts.length; i++) {
      html += options.callback.apply(window, parts[i]);
    }

    // In case of catastrophic failure, return the original text;
    return html || txt;
  };
})();

//QUICK AJAX SAVE
var _ajax = function () {
  this.queryString = '';
  this.url = '';
  this.method = 'POST';
  this.ajaxRequest;

  //INITIALIZE
  this.init = function () {
    this.ajaxRequest; // The variable that makes Ajax possible!
    try {
      this.ajaxRequest = new XMLHttpRequest(); // Opera 8.0+, Firefox, Safari
    } catch (e) {
      // Internet Explorer Browsers
      try {
        this.ajaxRequest = new ActiveXObject('Msxml2.XMLHTTP');
      } catch (e) {
        try {
          this.ajaxRequest = new ActiveXObject('Microsoft.XMLHTTP');
        } catch (e) {
          alert('Your browser broke!');
          return false; // Something went wrong
        }
      }
    }

    // Create a function that will receive data sent from the server
    this.ajaxRequest.onreadystatechange = function () {
      if (this.readyState == 4 && this.status == 200) {
        this.done();
      } else if (this.readyState == 4 && this.status == 0) {
        this.error();
      } else {
      }
    };

    this.ajaxRequest.error = this.error;
    this.ajaxRequest.done = this.response;
  };

  //SEND
  this.run = function () {
    if (this.url != '') {
      this.init();
      this.ajaxRequest.open(this.method, this.url, true);
      this.ajaxRequest.setRequestHeader(
        'Content-type',
        'application/x-www-form-urlencoded'
      );
      this.ajaxRequest.send(this.queryString);
    }
  };

  //ERROR
  this.error = function () {
    //console.log("There was an error, submitting again...");
    this.run();
  };

  //RESPONSE
  this.response = function () {};
};

function quick_save_ajax(url, qString, return_function) {
  return_function = return_function || false;

  var ajaxRequest; // The variable that makes Ajax possible!

  try {
    // Opera 8.0+, Firefox, Safari
    ajaxRequest = new XMLHttpRequest();
  } catch (e) {
    // Internet Explorer Browsers
    try {
      ajaxRequest = new ActiveXObject('Msxml2.XMLHTTP');
    } catch (e) {
      try {
        ajaxRequest = new ActiveXObject('Microsoft.XMLHTTP');
      } catch (e) {
        // Something went wrong
        alert('Your browser broke!');
        return false;
      }
    }
  }

  // Create a function that will receive data sent from the server
  ajaxRequest.onreadystatechange = function () {
    if (ajaxRequest.readyState != 4) {
    } else if (ajaxRequest.readyState == 4 && ajaxRequest.status == 200) {
      var ret = ajaxRequest.responseText;
      if (qString['what'] == 'project_status' && typeof element == 'object') {
        if (ret == '') {
        } else {
          custom_alert(ret);
        }
      } else if (qString['flag'] == 'edit_time') {
        //ADJUSTING START OR END TIME OF A PUNCH IN
        var response = eval('(' + ajaxRequest.responseText + ')');
        var input = $id(response.times[0].input);
        var duration = response.times[0].duration;
        if (input && duration != '') {
          input.value = format_time(duration)['formatted'];
        }
        edit_times_total();
      }

      if (return_function != false && typeof return_function == 'function') {
        return_function();
      }
    } else if (ajaxRequest.readyState == 4 && ajaxRequest.status == 0) {
      //RE RUN IF HTTP FAILS
      quick_save_ajax(url, qString);
    } else {
    }
  };

  var queryString = '';
  for (var q in qString) {
    queryString += queryString != '' ? '&' : '';
    queryString += q + '=' + tweak_text_for_get(qString[q]);
  }

  ajaxRequest.open('POST', url, true);
  ajaxRequest.setRequestHeader(
    'Content-type',
    'application/x-www-form-urlencoded'
  );
  ajaxRequest.send(queryString);
}

function edit_bookmarks(ele) {
  var div = $id('bookmarks');
  var direction = div.className.indexOf('edit') == -1 ? 'edit' : 'close';

  if (direction == 'edit') {
    div.className = 'edit';
    ele.firstChild.nodeValue = 'done editing';
  } else {
    div.className = '';
    ele.firstChild.nodeValue = 'edit my links';
  }
}
function bookmark_page() {
  click_current_backdrop();
  var url = get_is_embedded_view() ? window.parent.location : window.location;

  var html = '<h1>Bookmark Page:</h1>';
  html +=
    '<div>Bookmarking this page will place a link in your user dropdown for quick access.</div>';
  html +=
    "<div style='padding-top:1em;'>Bookmark Name: <input id='new_bookmark_name' type='text' size='30' value='' /></div>";

  var popup = custom_confirm(html);
  popup['no'].firstChild.nodeValue = 'cancel';
  popup['yes'].firstChild.nodeValue = 'Save Bookmark';
  popup['yes'].setAttribute('url', url);
  popup['yes'].onclick = function () {
    create_target('bookmark', {
      url: this.getAttribute('url'),
      name: $id('new_bookmark_name').value,
    });
    this.ondblclick();
  };

  setTimeout(function () {
    if ($id('new_bookmark_name')) {
      $id('new_bookmark_name').value = document.title.replace(
        ' | TeamGantt',
        ''
      );

      $id('new_bookmark_name').select();
    }
  }, 250);
}

function delete_bookmark(id) {
  var conf = confirm('Are you sure you want to delete this bookmark?');
  if (conf) {
    delete_target('bookmark', id);
    $id('bookmark_' + id).parentNode.removeChild($id('bookmark_' + id));
  }

  event.preventDefault();
}

var _target_options_xml = null;
function load_new_selector(which) {
  var ajaxRequest; // The variable that makes Ajax possible!

  try {
    // Opera 8.0+, Firefox, Safari
    ajaxRequest = new XMLHttpRequest();
  } catch (e) {
    // Internet Explorer Browsers
    try {
      ajaxRequest = new ActiveXObject('Msxml2.XMLHTTP');
    } catch (e) {
      try {
        ajaxRequest = new ActiveXObject('Microsoft.XMLHTTP');
      } catch (e) {
        // Something went wrong
        alert('Your browser broke!');
        return false;
      }
    }
  }

  // Create a function that will receive data sent from the server
  ajaxRequest.onreadystatechange = function () {
    if (ajaxRequest.readyState != 4) {
    } else if (ajaxRequest.readyState == 4 && ajaxRequest.status == 200) {
      _target_options_xml = ajaxRequest.responseXML;
      build_selector(which);

      if (which == 'comment') {
        $id('new_comment_button').onclick = function () {
          load_new_selector('comment');
        };
      }
    } else {
    }
  };

  if (which == 'comment') {
    $id('new_comment_button').onclick = null;
  }

  build_selector_preload(which);

  var queryString = 'ids=' + tweak_text_for_get($id('project_ids').value);

  ajaxRequest.open('POST', '../includes/xml.search_project_data.php', true);
  ajaxRequest.setRequestHeader(
    'Content-type',
    'application/x-www-form-urlencoded'
  );
  ajaxRequest.send(queryString);
}

function build_selector_preload(which) {
  if ($id('new_selector')) {
    if ($id('new_selector').parentNode.id == 'comment_location') {
      $id('new_selector').parentNode.className = 'hidden';
      remove_child_nodes($id('new_selector').parentNode);
    } else {
      $id('new_selector').parentNode.removeChild($id('new_selector'));
    }
  }

  if (which == 'comment') {
    var parent_div = $id('comment_location');
  } else if (which == 'document') {
    var parent_div = $id('upload_docs');
  } else {
    var parent_div = $id('search_task');
    var background = build_background_cover();
    background.id = 'search_task_background';
    background.onclick = function () {
      $id('search_task').className = 'hidden';
      remove_child_nodes($id('search_task'));
      this.parentNode.removeChild(this);
    };
  }

  var div = $create('DIV');
  div.id = 'new_selector';
  remove_child_nodes(parent_div);
  parent_div.appendChild(div);
  parent_div.className = '';

  //H TAG
  if (which == 'comment') {
    var h2 = $create('H2');
    h2.appendChild($text('Start a New Conversation'));
    h2.style.top = '-0.15em';
    parent_div.appendChild(h2);
  }

  //SUBNOTE
  var sub_note_target = which == 'comment' ? 'conversation' : '';
  sub_note_target = which == 'document' ? 'document' : which;
  sub_note_target = which == 'time-tracking' ? 'time' : which;

  var sub_note = $create('DIV');
  sub_note.className = 'search_note';
  sub_note.appendChild(
    $text(
      'Select a project, group, or task for the ' +
        sub_note_target +
        ' to be linked to:'
    )
  );
  div.appendChild(sub_note);

  //SEARCH
  var input = $create('INPUT');
  input.id = 'new_selector_search';
  input.setAttribute('placeholder', 'Search...');
  input.onkeyup = function () {
    filter_search();
  };
  div.appendChild(input);

  input.focus();

  //LOCATION
  var target = $create('DIV');
  target.id = 'new_selector_options';
  div.appendChild(target);
}

function build_selector(which) {
  var xml = _target_options_xml;
  var div = $id('new_selector');
  var target = $id('new_selector_options');

  //PUT ITEMS IN PLACE
  var opts = xml.getElementsByTagName('OPTIONS')[0].childNodes;
  for (i = 0; i < opts.length; i++) {
    var ele = $create('DIV');
    var name = opts[i].firstChild ? opts[i].firstChild.nodeValue : '';

    if (opts[i].tagName == 'PROJECT') {
      ele.className = 'project';
      ele.id = 'select_project_' + opts[i].getAttribute('id');
      ele.setAttribute('target', 'project');
      ele.setAttribute('target_id', opts[i].getAttribute('id'));
      ele.setAttribute('project_id', opts[i].getAttribute('project_id'));
      ele.setAttribute('which', which);
      ele.onclick = function () {
        if (this.getAttribute('which') == 'comment') {
          enter_new_comment(this);
          if ($id('new_selector')) {
            $id('new_selector').parentNode.removeChild($id('new_selector'));
          }
        } else if (this.getAttribute('which') == 'document') {
          _projects = false;
          upload_new_document(this);
          if ($id('new_selector')) {
            $id('new_selector').parentNode.removeChild($id('new_selector'));
          }
        }
      };
      ele.appendChild($text(name));

      target.appendChild(ele);
    } else if (opts[i].tagName == 'GROUP') {
      ele.className = 'group';
      ele.id = 'select_group_' + opts[i].getAttribute('id');
      ele.setAttribute('target', 'group');
      ele.setAttribute('target_id', opts[i].getAttribute('id'));
      ele.setAttribute('project_id', opts[i].getAttribute('project_id'));
      ele.setAttribute('which', which);
      ele.setAttribute(
        'parent_id',
        opts[i].getAttribute('parent_group') == ''
          ? 'select_project_' + opts[i].getAttribute('project_id')
          : 'select_group_' + opts[i].getAttribute('parent_group')
      );
      ele.onclick = function () {
        if (this.getAttribute('which') == 'comment') {
          enter_new_comment(this);
          if ($id('new_selector')) {
            $id('new_selector').parentNode.removeChild($id('new_selector'));
          }
        } else if (this.getAttribute('which') == 'document') {
          _groups = false;
          upload_new_document(this);
          if ($id('new_selector')) {
            $id('new_selector').parentNode.removeChild($id('new_selector'));
          }
        }
      };
      ele.appendChild($text(name));
      ele.style.textIndent = opts[i].getAttribute('indents') * 0.75 + 'em';

      target.appendChild(ele);
    } else if (opts[i].tagName == 'TASK') {
      ele.className = 'task';
      ele.id = 'select_task_' + opts[i].getAttribute('id');
      ele.setAttribute('target', 'task');
      ele.setAttribute('target_id', opts[i].getAttribute('id'));
      ele.setAttribute('project_id', opts[i].getAttribute('project_id'));
      ele.setAttribute('assigned_people', opts[i].getAttribute('assigned'));
      ele.setAttribute('which', which);
      ele.onclick = function () {
        if (this.getAttribute('which') == 'comment') {
          enter_new_comment(this);
          if ($id('new_selector')) {
            $id('new_selector').parentNode.removeChild($id('new_selector'));
          }
        } else if (this.getAttribute('which') == 'document') {
          upload_new_document(this);
          if ($id('new_selector')) {
            $id('new_selector').parentNode.removeChild($id('new_selector'));
          }
        } else if (this.getAttribute('which') == 'time-tracking') {
          edit_times(this.getAttribute('target_id'));
          $id('search_task').className = 'hidden';
          $id('search_task_background').parentNode.removeChild(
            $id('search_task_background')
          );
          if ($id('new_selector')) {
            $id('new_selector').parentNode.removeChild($id('new_selector'));
          }
        }
      };
      ele.setAttribute(
        'parent_id',
        'select_group_' + opts[i].getAttribute('parent_group')
      );
      ele.appendChild($text(name));
      ele.style.textIndent =
        (opts[i].getAttribute('indents') * 1 + 1) * 0.75 + 'em';

      target.appendChild(ele);
    }
  }

  filter_search();
  if (typeof position_comment_window == 'function') {
    position_comment_window(div);
  }

  $id('new_selector_search').focus();
}

function filter_search() {
  var input = $id('new_selector_search').value;
  var divs = $id('new_selector_options').getElementsByTagName('DIV');

  //FILTER TO JUST WHAT SHOWS
  for (var d = 0; d < divs.length; d++) {
    divs[d].setAttribute('show', 0);
    divs[d].className = trim(divs[d].className.replace(/show_grey/g, ''));
    divs[d].className = trim(divs[d].className.replace(/highlight/g, ''));
    divs[d].className = trim(divs[d].className.replace(/hidden/g, ''));

    if (input == '') {
    } else if (
      divs[d].firstChild &&
      strip_spaces(divs[d].firstChild.nodeValue).indexOf(strip_spaces(input)) >
        -1
    ) {
      if (
        _version == 'time-tracking' &&
        (divs[d].className.indexOf('group') > -1 ||
          divs[d].className.indexOf('project') > -1)
      ) {
        //CAN'T SEARCH ON GROUP OR PROJECT IN TIME TRACKING
        divs[d].className += ' hidden';
      } else {
        divs[d].className += ' highlight';
        divs[d].setAttribute('show', 1);
      }
    } else {
      divs[d].className += ' hidden';
    }
  }

  //DISPLAY PARENTS
  for (var d = 0; d < divs.length; d++) {
    if (divs[d].getAttribute('show') == 1) {
      display_parent(divs[d]);
    }
  }
}

function strip_spaces(string) {
  return string.toLowerCase().replace(/\s+/g, '');
}

function display_parent(div) {
  if (div.getAttribute('parent_id') != '') {
    var parent = $id(div.getAttribute('parent_id'));
    if (parent && parent.getAttribute('show') == 0) {
      parent.className = trim(parent.className.replace(/hidden/g, ''));
      parent.className += ' show_grey';

      display_parent(parent);
    }
  }
}

function random_string(length) {
  length = length || 5;
  var text = '';
  var possible =
    'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';

  for (var i = 0; i < length; i++)
    text += possible.charAt(Math.floor(Math.random() * possible.length));

  return text;
}

/***** API AJAX *****/
function $ajax(request) {
  request.async = request.async || true;
  window.teamgantt.auth.currentSession().then(
    function (session) {
      var cognitoBearer = session.getToken();
      var ajaxRequest; // The variable that makes Ajax possible!

      try {
        // Opera 8.0+, Firefox, Safari
        ajaxRequest = new XMLHttpRequest();
      } catch (e) {
        // Internet Explorer Browsers
        try {
          ajaxRequest = new ActiveXObject('Msxml2.XMLHTTP');
        } catch (e) {
          try {
            ajaxRequest = new ActiveXObject('Microsoft.XMLHTTP');
          } catch (e) {
            // Something went wrong
            alert('Your browser broke!');
            return false;
          }
        }
      }

      // Create a function that will receive data sent from the server
      ajaxRequest.onreadystatechange = function () {
        if (ajaxRequest.readyState == 4) {
          if (ajaxRequest.status === 0 && !$id('custom_alert_cover')) {
            var okButton = custom_alert("Oh no! It looks like you're offline!");
            remove_child_nodes(okButton);
            okButton.appendChild($text('Refresh'));
            okButton.onclick = function () {
              window.location.reload();
            };
          }
          request.response(ajaxRequest);
        }
      };

      if (request.type && request.url) {
        ajaxRequest.open(request.type, request.url, true);
        ajaxRequest.setRequestHeader('Content-type', 'application/json');

        var publicKeys = get_public_keys();
        var projectIds = $id('project_ids') ? $id('project_ids').value : '';

        if (cognitoBearer) {
          ajaxRequest.setRequestHeader(
            'Authorization',
            'Bearer ' + cognitoBearer
          );
        } else if (publicKeys !== '' && projectIds !== '') {
          ajaxRequest.setRequestHeader(
            'TG-Authorization-ProjectIds',
            projectIds
          );
          ajaxRequest.setRequestHeader(
            'TG-Authorization-PublicKeys',
            publicKeys
          );
        }
        ajaxRequest.send(JSON.stringify(request.data));
      }
    },
    function (authError) {
      if (_is_iframe_view !== undefined && _is_iframe_view === true) {
        return;
      }

      var okButton = custom_alert('Your session expired. Please log in again.');
      okButton.onclick = function () {
        window.location =
          NEW_APP_URL +
          'auth?redirectTo=' +
          encodeURIComponent(window.location.href);
      };
    }
  );
}

// set a cookie value, stolen from https://www.w3schools.com/js/js_cookies.asp
function setCookie(cname, cvalue, exdays) {
  var d = new Date();
  d.setTime(d.getTime() + exdays * 24 * 60 * 60 * 1000);
  var expires = 'expires=' + d.toUTCString();

  document.cookie =
    cname + '=' + cvalue + ';' + expires + ';path=/;domain=.teamgantt.com';
}

// get a cookie value, stolen from https://www.w3schools.com/js/js_cookies.asp
function getCookie(cname) {
  var name = cname + '=';
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for (var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return '';
}

/***** END API AJAX *****/

/***** GLOBAL TIME TRACKER *******/
function format_time(input) {
  var input = input.toString();
  var is_neg = input.indexOf('-') > -1 ? true : false;
  input = input.replace('-', '');
  input = input.replace(/,/g, '.');

  //BRING INPUT TO DECIMAL FORMAT
  if (input.indexOf(':') > -1) {
    //SPLIT INPUT
    var parts = input.split(':');
    var hours = parts[0] * 1;
    var minutes = parts[1] ? parts[1] * 1 : 0;

    //IF MINUTES IS MORE THAN ONE HOUR
    if (minutes > 60) {
      hours = hours + Math.round(minutes / 60);
      minutes = minutes % 60;
    }

    //CONVERT MINUTES TO NUMBER (multiply by 100 for rounding, then divide by 100 for decimal representation
    minutes = Math.round((minutes / 60) * 10000);
    minutes = minutes / 10000;

    var decimal_extended = hours + minutes;
    input = hours + minutes;
  } else {
    var decimal_extended = parseFloat(input);
  }

  // FORMAT DECIMAL EXTENDED
  if (is_neg) {
    decimal_extended = decimal_extended * -1;
  }

  input = Math.round(input * 100) / 100;

  //RETURN ARRAY
  var array = [];
  array['hours'] = 0;
  array['minutes'] = 0;
  array['formatted'] = '00:00';
  array['decimal'] = input;
  array['decimal_extended'] = decimal_extended;

  //BREAK IT UP
  var parts = input.toString().split('.');
  var hours = parts[0] * 1;
  var minutes = parts[1] ? ('0.' + parts[1]) * 1 : 0;
  var real_minutes = to_two(Math.round((minutes * 60).toString())); //round off to get the right time
  var formatted = hours + ':' + real_minutes;
  var minutes = real_minutes;

  if (is_neg) {
    hours = hours * -1;
    minutes = minutes * -1;
    formatted = '-' + formatted;
    array['decimal'] = array['decimal'] * -1;
  }

  array['hours'] = hours;
  array['minutes'] = minutes;
  array['formatted'] = formatted;

  return array;
}

function global_time_tracker(user_id) {
  user_id = user_id || $id('header').getAttribute('user_id');
  this.user_id = user_id;
  this.icon = null;
  this.attrs = {
    parent: this,
    set: function (attrs) {
      this.values = attrs;
      this.parent.update_icon();
      return this.values;
    },
  };
  this.status = {
    parent: this,
    value: null,
    set: function (status) {
      this.value = status;
      this.parent.update_icon();
      return this.value;
    },
  };
  this.div;
  this.elements = {};
  this.selected_task_id = null;
  this.tasks = [];

  this.did_init = false;

  this.class_name = function () {
    for (var name in this.global) {
      if (this.global[name] == this) {
        return name;
      }
    }
  };
}

global_time_tracker.prototype.global = this;

global_time_tracker.prototype.init = function () {
  this.did_init = true;

  this.icon = $id('global_time_tracker_icon');
};

global_time_tracker.prototype.fetch_current = function () {
  if (!this.did_init) {
    this.init();
  }

  new $ajax({
    parent: this,
    type: 'GET',
    url: API_URL + 'v1/times?current',
    response: function (data) {
      if (data.status == 204) {
        this.parent.status.set('not_punched_in');
      } else {
        var json = json_decode(data.responseText);
        this.parent.attrs.set(json);
        this.parent.status.set('punched_in');
        this.parent.selected_task_id = json.task_id;
      }
    },
  });

  if (
    typeof get_is_embedded_view === 'function' &&
    get_is_embedded_view() === true
  ) {
    parent_post_message('refresh-global-time-tracker');
  }
};

global_time_tracker.prototype.update_icon = function () {
  this.icon.className = this.status.value;
  remove_child_nodes(this.icon);
  if (this.status.value == 'not_punched_in') {
    this.icon.setAttribute('js_class', this.class_name());
    this.icon.onclick = function () {
      var gtt_class = window[this.getAttribute('js_class')];
      gtt_class.open_window('punch_in');
    };
  } else if (this.status.value == 'punched_in') {
    var name = this.attrs.values.task_name;
    if (name.length > 30) {
      name = trim(name.substring(0, 27)) + '...';
    }

    var span = $create('SPAN');
    span.className = 'task_name';
    span.appendChild($text(name));
    this.icon.appendChild(span);

    this.icon.title = this.attrs.values.task_name;
    var time_diff = time_difference(this.attrs.values.start_time, Date());
    if (time_diff.indexOf('-') > -1) {
      time_diff = '00:00';
    }
    var duration = $create('SPAN');
    duration.className = 'duration';
    var i = $create('I');
    i.className = 'fa fa-clock-o';
    i.className = 'punched_in_clock';
    duration.appendChild(i);
    duration.appendChild($text(' ' + time_diff));
    this.icon.appendChild(duration);

    this.icon.setAttribute('js_class', this.class_name());
    this.icon.onclick = function () {
      window[this.getAttribute('js_class')].open_window('punch_out');
    };

    setTimeout(this.update_icon.bind(this), 15000);
  }
};

global_time_tracker.prototype.open_window = function (which) {
  var rect = this.icon.parentNode.getBoundingClientRect();
  var gtt_top = rect.height;
  var gtt_right = window.innerWidth - rect.right;

  open_iframe_overlay('global_time_tracker', gtt_top, gtt_right);
};

/***** END GLOBAL TIME TRACKER *******/

function upgrade_popup() {
  var html = '';

  html +=
    "<div class='popup_banner'>You are currently on the FREE plan. It’s free forever, but if you want more...</div>";

  html += '<h2>Upgrade today to get access to:</h2>';

  html += "<div class='bullet_point'>Unlimited projects</div>";
  html += "<div class='bullet_point'>More Users</div>";
  html += "<div class='bullet_point'>Unlimited Resources</div>";
  html += "<div class='bullet_point'>Custom branded PDFs</div>";
  html += "<div class='bullet_point'>Project History and Undo</div>";
  html += "<div class='bullet_point'>Custom Project Templates</div>";
  html +=
    "<div class='bullet_point'>Baselines: Compare Estimated Plan vs Actual Plan</div>";
  html += "<div class='bullet_point'>Time Tracking</div>";
  html += "<div class='bullet_point'>Hourly Estimating</div>";

  html += "<div class='action_controls'>";
  html += "<a href='/gantt/purchase/' class='blue_button'>UPGRADE TODAY</a>";
  html +=
    "<span>or <u onclick='upgrade_popup_contact_sales();'>contact sales</u> for a demo or questions about pricing.</span>";
  html += '</div>';

  var div = custom_confirm(html);
  div['div'].parentNode.className = 'upgrade_plan';
  div['yes'].style.display = 'none';
  div['no'].style.display = 'none';
  div['ele'].style.background = 'rgba(50, 56, 68, .84)';
  div['ele'].onclick = function () {
    this.parentNode.removeChild(this);
  };

  div['div'].parentNode.onclick = function (e) {
    e.stopPropagation();
  };
}

function upgrade_popup_contact_sales() {
  $id('custom_alert_message').parentNode.click();
  open_intercom();
}

function logout_user() {
  navigate_window(NEW_APP_URL + 'logout');
}

function get_public_keys() {
  var public_keys_element = $id('public_keys');

  if (!public_keys_element) {
    return '';
  }

  return decodeURIComponent(public_keys_element.value);
}

function get_share_key() {
  var share_key_element = $id('share_key');

  if (!share_key_element) {
    return '';
  }

  return decodeURIComponent(share_key_element.value);
}
