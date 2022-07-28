<!DOCTYPE html>
<?php
  /**
   * The main template file
   *
   * @package Hey
   * @subpackage Heya
   */

  $email = "avigailk12357@gmail.com";
  $ig = "motherfucking_hell_yeah_bitch";
?>
<?php get_header(); ?>

<?php function contact_detail($text, $href) {?>
  <a class="detail disguise-links" href="<?= $href ?>" target="_blank" dir="ltr"
    style="grid-template-columns: repeat(<?= round(strlen($text) / 2) ?>, 1fr)">

    <?php foreach (str_split($text) as $letter) { ?>
      <div><?= $letter ?></div>
    <?php } ?>
  </a>
<?php } ?>

<div class="index-page">
  <div class="index-links cool-bg">
    <a href="/tattoos" class="pic-with-text-underneath disguise-links">
      <img src="<?= get_theme_file_uri('assets/ink.webp') ?>" alt="tattoos"/>
      <div> קעקועים </div>
    </a>
    <div class="spacer"></div>
    <a href="/makeup" class="pic-with-text-underneath disguise-links">
      <img src="<?= get_theme_file_uri('assets/fairyglitter.webp') ?>" alt="makeup"/>
      <div> איפור </div>
    </a>
  </div>

  <div class="contact-details cool-bg" dir="rtl">
    <img class="phone-pic" src="<?= get_theme_file_uri('assets/phone.webp') ?>" alt="phone">
    <?= contact_detail($email, "mailto:$email") ?>
    <?= contact_detail("@$ig", "https://instagram.com/$ig")?>
  </div>

  <div class="cool-bg bio" dir="rtl">
    הייי אני אביגיל
    <span class="emote" dir="ltr">( ͡ಠ ͜ つ ͡ಠ)</span>
    מאפר בוגר קורס איל מקיאז׳ וגם מקעקע מהצד!
    שלחו הודעה או מייל ונעשה חגיגה בסגנון מרוקאי
    <span class="emote wide" dir="ltr">(°͜ʖ͡°)╭∩╮</span>
  </div>
</div>

<?php get_footer(); ?>
