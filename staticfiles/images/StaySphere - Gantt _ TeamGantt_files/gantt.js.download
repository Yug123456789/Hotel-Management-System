// JavaScript Document

//APPEND CSS FILE
if (typeof load_gantt != "function") {
  var style = document.createElement("LINK");
  style.setAttribute("rel", "stylesheet");
  style.setAttribute("type", "text/css");
  style.setAttribute("href", "https://prod.teamgantt.com/gantt/public/css.css");

  document.getElementsByTagName("head")[0].appendChild(style);
}

//THE FRAME FUNCTION
function tgframe(tg) {
  tg = tgframe_clean(tg);

  //OPENING DIV
  document.write(
    "<div style='width:" +
      tg.width +
      "; " +
      tg.div_style +
      "' class='teamgantt_div " +
      tg.position +
      "'>"
  );

  //IFRAME
  document.write(
    "<iframe src='" +
      tg.src +
      "' style='height:" +
      tg.height +
      ";' frameborder='0' class='teamgantt_iframe'></iframe>"
  );

  //A LINK
  document.write(
    "<a href='http://teamgantt.com/' target='_blank' class='teamgantt_iframe_anchor'>powered by TeamGantt</a>"
  );

  //CLOSE DIV
  document.write("</div>");
}

function tgframe_clean(tg) {
  function clean_size(size) {
    if (size) {
      size = size.toString();
      if (size.indexOf("%") > -1) {
        return size;
      } else if (size.indexOf("px") > -1) {
        return size;
      } else {
        return size + "px";
      }
    }
  }

  //SET DEFAULT VALUES
  tg.id = tg.id || [];
  tg.key = tg.key || [];
  tg.width = tg.width || "100%";
  tg.width = clean_size(tg.width);
  tg.height = tg.height || "600px";
  tg.height = clean_size(tg.height);
  tg.position = tg.position || "center";
  tg.zoom = tg.zoom || "d100";
  tg.font_size = tg.font_size || 11;
  tg.estimated_hours = tg.estimated_hours || "0";
  tg.assigned_resources = tg.assigned_resources || "0";
  tg.percent_complete = tg.percent_complete || "0";
  tg.documents = tg.documents || "0";
  tg.comments = tg.comments || "0";
  tg.col_width = tg.col_width || "355px";
  tg.div_style = tg.div_style || "";
  tg.public_hide_header_tabs = tg.public_hide_header_tabs || "0";
  tg.public_show_menu_view = tg.public_show_menu_view || "1";
  tg.public_task_resource_names = tg.public_task_resource_names || "1";
  tg.public_task_resource_hours_per_day =
    tg.public_task_resource_hours_per_day || "1";
  tg.public_show_resource_filter = tg.public_show_resource_filter || "1";
  tg.apply_filters = tg.apply_filters || false;

  //TASK NAME
  var show_task_name = tg.public_task_name_in_bar || "0";
  if (show_task_name == 1) {
    tg.public_task_name_in_bar = 1;
    tg.public_task_name_next_to_bar = 0;
  } else if (show_task_name == 2) {
    tg.public_task_name_in_bar = 0;
    tg.public_task_name_next_to_bar = 1;
  }
  tg.public_task_name_in_bar = tg.public_task_name_in_bar || "0";
  tg.public_task_name_next_to_bar = tg.public_task_name_next_to_bar || "0";

  var src =
    APP_URL +
    "gantt/schedule/?ids=" +
    tg.id.join(",") +
    "&public_keys=" +
    tg.key.join(",");
  src += "&zoom=" + tg.zoom;
  src += "&font_size=" + tg.font_size;
  src += "&estimated_hours=" + tg.estimated_hours;
  src += "&assigned_resources=" + tg.assigned_resources;
  src += "&percent_complete=" + tg.percent_complete;
  src += "&documents=" + tg.documents;
  src += "&comments=" + tg.comments;
  src += "&col_width=" + tg.col_width;
  src += "&hide_header_tabs=" + tg.public_hide_header_tabs;
  src += "&menu_view=" + tg.public_show_menu_view;
  src += "&resource_filter=" + tg.public_show_resource_filter;
  src += "&name_in_bar=" + tg.public_task_name_in_bar;
  src += "&name_next_to_bar=" + tg.public_task_name_next_to_bar;
  src += "&resource_names=" + tg.public_task_resource_names;
  src += "&resource_hours=" + tg.public_task_resource_hours_per_day;

  if (tg.apply_filters == "true") {
    hsrc =
      "#user=" +
      (HashSearch.keyExists("user") == true ? HashSearch.get("user") : "");
    hsrc +=
      "&company=" +
      (HashSearch.keyExists("company") == true
        ? HashSearch.get("company")
        : "");
    hsrc +=
      "&custom=" +
      (HashSearch.keyExists("custom") == true ? HashSearch.get("custom") : "");
    hsrc +=
      "&date_filter=" +
      (HashSearch.keyExists("date_filter") == true
        ? HashSearch.get("date_filter")
        : "");
    hsrc +=
      "&hide_completed=" +
      (HashSearch.keyExists("hide_completed") == true
        ? HashSearch.get("hide_completed")
        : "");
    hsrc +=
      "&color_filter=" +
      (HashSearch.keyExists("color_filter") == true
        ? HashSearch.get("color_filter")
        : "");

    src += hsrc;
  }
  tg.src = src;

  return tg;
}
