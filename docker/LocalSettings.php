<?php

/******************************/
/* EurHisFirm custom settings */
/******************************/
$wgSitename = "AlpesTransport-wikibase";

# Disable account creation and anonymous edits
# https://stuff.coffeecode.net/2018/wikibase-workshop-swib18.html#_disabling_account_creation_and_anonymous_edits
// $wgGroupPermissions['*']['edit'] = false;
// $wgGroupPermissions['*']['createaccount'] = false;

# AlpesTransport Logo
$wgLogo = "$wgResourceBasePath/assets/logo_wb.png";

# Footer with image
# Docs: https://www.mediawiki.org/wiki/Manual:$wgFooterIcons
$wgFooterIcons = [
    "copyright" => [
        "copyright" => [], // placeholder for the built in copyright icon
    ],
    "poweredby" => [
        "mediawiki" => [
            "src" => "$wgResourceBasePath/assets/footer-ce.png",
            "height" => "75",
            "width" => "200",
		],
	],
];


$wgDefaultUserPassword = 'adminpass';