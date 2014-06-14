<?php
/**
 * The base configurations of the WordPress.
 *
 * This file has the following configurations: MySQL settings, Table Prefix,
 * Secret Keys, WordPress Language, and ABSPATH. You can find more information
 * by visiting {@link http://codex.wordpress.org/Editing_wp-config.php Editing
 * wp-config.php} Codex page. You can get the MySQL settings from your web host.
 *
 * This file is used by the wp-config.php creation script during the
 * installation. You don't have to use the web site, you can just copy this file
 * to "wp-config.php" and fill in the values.
 *
 * @package WordPress
 */

// ** MySQL settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define('DB_NAME', '');

/** MySQL database username */
define('DB_USER', '');

/** MySQL database password */
define('DB_PASSWORD', '');

/** MySQL hostname */
define('DB_HOST', '');

/** Database Charset to use in creating database tables. */
define('DB_CHARSET', 'utf8');

/** The Database Collate type. Don't change this if in doubt. */
define('DB_COLLATE', '');

//url settings
define('WP_HOME','');
define('WP_SITEURL','');

/**#@+
 * Authentication Unique Keys and Salts.
 *
 * Change these to different unique phrases!
 * You can generate these using the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}
 * You can change these at any point in time to invalidate all existing cookies. This will force all users to have to log in again.
 *
 * @since 2.6.0
 */
define('AUTH_KEY',         '*ASBAqJ![edmy3=+]|}$.gNo8JkZ`yjYDw/l-${<j{<}n7`yCa6xr![1%!bhu.+`');
define('SECURE_AUTH_KEY',  'S~H4uI@ A`7HY<%%v-]D,_!C EX6>+2U)Co/$,++Y>&IDzF[/2 W6j@3HeA|vH!U');
define('LOGGED_IN_KEY',    'zoB1U?|-7r07[MbYg!ZU((R>7-vFo#L_Aw1|-B9A=rAy*P:ArsG31~`B(VxIncr$');
define('NONCE_KEY',        'T6,OI+,TX*sHm;Da(-qlzgWP+di#QL 2au{hZg}@=/nIR-7v{8L&[8N?5.Gh`88|');
define('AUTH_SALT',        '1aw&0M]P&;#3Kl6Q1?a++R,U5Q`&%%YOe|#a$P $(j(Y[,B#&*U+d ao5fdR}[8;');
define('SECURE_AUTH_SALT', 'R,J:dmn7,tKeC]oQO7%o?/bC6=H|lB)||;V|Cq#pI0)mjglaS?fD6,lx+MEiem1[');
define('LOGGED_IN_SALT',   '8iohG13Hl|>3B|`;+ <@3`@38A;N3X+ze-Bt~9(bL7dQCl)ZlD.A8q*+(,xPbMs:');
define('NONCE_SALT',       'avO)I?UacAX<}PS#E9[-P#yuB+Ao#}e<Vk^VbP:z-A9Y3bcp GI}khE*7N8vtF(|');

/**#@-*/

/**
 * WordPress Database Table prefix.
 *
 * You can have multiple installations in one database if you give each a unique
 * prefix. Only numbers, letters, and underscores please!
 */
$table_prefix  = 'wp_';

/**
 * WordPress Localized Language, defaults to English.
 *
 * Change this to localize WordPress. A corresponding MO file for the chosen
 * language must be installed to wp-content/languages. For example, install
 * de_DE.mo to wp-content/languages and set WPLANG to 'de_DE' to enable German
 * language support.
 */
define('WPLANG', 'sv_SE');

/**
 * For developers: WordPress debugging mode.
 *
 * Change this to true to enable the display of notices during development.
 * It is strongly recommended that plugin and theme developers use WP_DEBUG
 * in their development environments.
 */
define('WP_DEBUG', false);

/* That's all, stop editing! Happy blogging. */

/** Absolute path to the WordPress directory. */
if ( !defined('ABSPATH') )
	define('ABSPATH', dirname(__FILE__) . '/');

/** Sets up WordPress vars and included files. */
require_once(ABSPATH . 'wp-settings.php');
