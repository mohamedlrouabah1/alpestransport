<?php
/**
 * ----------------------------------------------------------------------------------------
 * This file is provided by the wikibase/wikibase docker image.
 * This file will be passed through envsubst which will replace "${DOLLAR}" with "$".
 * If you want to change MediaWiki or Wikibase settings then either mount a file over this
 * template and or run a different entrypoint.
 * ----------------------------------------------------------------------------------------
 */

/******************************/
/* AlpesTransport custom settings */
/******************************/
${DOLLAR}wgSitename = "AlpesTransport";

## Database settings
## Environment variables will be substituted in here.
${DOLLAR}wgDBserver = "${DB_SERVER}";
${DOLLAR}wgDBname = "${DB_NAME}";
${DOLLAR}wgDBuser = "${DB_USER}";
${DOLLAR}wgDBpassword = "${DB_PASS}";

## Logs
## Save these logs inside the container
${DOLLAR}wgDebugLogGroups = array(
	'resourceloader' => '/var/log/mediawiki/resourceloader.log',
	'exception' => '/var/log/mediawiki/exception.log',
	'error' => '/var/log/mediawiki/error.log',
);

## Site Settings
# TODO pass in the rest of this with env vars?
${DOLLAR}wgServer = WebRequest::detectServer();
${DOLLAR}wgShellLocale = "en_US.utf8";
${DOLLAR}wgLanguageCode = "${MW_SITE_LANG}";
${DOLLAR}wgSitename = "${MW_SITE_NAME}";
${DOLLAR}wgMetaNamespace = "Project";
# Configured web paths & short URLs
# This allows use of the /wiki/* path
## https://www.mediawiki.org/wiki/Manual:Short_URL
${DOLLAR}wgScriptPath = "/w";        // this should already have been configured this way
${DOLLAR}wgArticlePath = "/wiki/${DOLLAR}1";

#Set Secret
${DOLLAR}wgSecretKey = "${MW_WG_SECRET_KEY}";

## RC Age
# https://www.mediawiki.org/wiki/Manual:$wgRCMaxAge
# Items in the recentchanges table are periodically purged; entries older than this many seconds will go.
# The query service (by default) loads data from recent changes
# Set this to 1 year to avoid any changes being removed from the RC table over a shorter period of time.
${DOLLAR}wgRCMaxAge = 365 * 24 * 3600;

wfLoadSkin( 'Vector' );




# AlpesTransport Logo
${DOLLAR}wgLogo = "$wgResourceBasePath/assets/logo_wb.png";

# Footer with image
# Docs: https://www.mediawiki.org/wiki/Manual:$wgFooterIcons
${DOLLAR}wgFooterIcons = [
    "copyright" => [
        "copyright" => [], // placeholder for the built in copyright icon
    ],
    "poweredby" => [
        "mediawiki" => [
            "src" => ${DOLLAR}wgResourceBasePath"/assets/footer-ce.png",
            "height" => "75",
            "width" => "200",
		],
	],
];
## Wikibase
# Load Wikibase repo & client with the example / default settings.
require_once "${DOLLAR}IP/extensions/Wikibase/repo/Wikibase.php";
require_once "${DOLLAR}IP/extensions/Wikibase/repo/ExampleSettings.php";
require_once "${DOLLAR}IP/extensions/Wikibase/client/WikibaseClient.php";
require_once "${DOLLAR}IP/extensions/Wikibase/client/ExampleSettings.php";
