<?php
  get_header();
  $src = wp_get_attachment_image_src(get_post_thumbnail_id(), 'full')[0];
  $next_post = get_next_post();
  $prev_post = get_previous_post();
?>
<div class="pic-page">
  <div class="pic-page-nav">
    <?php if ($next_post): ?>
      <a href="<?= $next_post->guid ?>" class="direction disguise-links cool-bg">
        <img src="<?= get_theme_file_uri('assets/left.webp') ?>">
        <div dir="rtl">לתמונה הבאה!!</div>
      </a>
    <?php endif; ?>

    <div class="spacer"></div>

    <?php if ($prev_post): ?>
      <a href="<?= $prev_post->guid ?>" class="direction disguise-links cool-bg">
        <img src="<?= get_theme_file_uri('assets/right.webp') ?>">
        <div dir="rtl">לתמונה הקודמת!!</div>
      </a>
    <?php endif; ?>
  </div>
  <img class="pic-page-main-pic" src="<?= $src ?>" />
</div>
<?php get_footer(); ?>
