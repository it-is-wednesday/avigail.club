<?php
add_action("init", function () {
    register_post_type("tattoos", [
        "labels" => ["menu_name" => "Tattoos"],
        "has_archive" => true,
        "public" => true,
        "supports" => ["title", "thumbnail"],
        "menu_icon" => "dashicons-color-picker",
        "rewrite" => ["with_front" => false],
    ]);
    register_post_type("makeup", [
        "labels" => ["menu_name" => "Makeup"],
        "has_archive" => true,
        "public" => true,
        "supports" => ["title", "thumbnail"],
        "menu_icon" => "dashicons-admin-customizer",
        "rewrite" => ["with_front" => false],
    ]);
});

add_action("admin_init", function () {
    remove_menu_page("edit.php");
    remove_menu_page("plugins.php");
    remove_menu_page("edit-comments.php");
});

add_action("after_setup_theme", function () {
    add_theme_support("post-thumbnails");
});

// cool numeric post links
add_filter(
    "post_type_link",
    function ($post_link, $post = 0) {
        $type = $post->post_type;
        if ($type === "makeup" || $type == "tattoos") {
            return home_url("{$type}/" . $post->ID . "/");
        } else {
            return $post_link;
        }
    },
    1,
    3
);

/*
 * Local Variables:
 * mode: php
 * End:
 * End: */
