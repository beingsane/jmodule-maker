<?php

/* 
 * MODULE: mod_tmp
 * AUTHOR: author_tmp
 * VERSION: version_tmp
 * 
 * Unauthorized copying of this file, via any medium is strictly prohibited
 * Proprietary and confidential
 * Copyright (c) year_tmp, SM Retail, Inc.
 * All rights reserved.
 */


// No direct access
defined('_JEXEC') or die;
// Include the syndicate function only once
require_once dirname(__FILE__) . '/helper.php';

$z = ModNameTmpHelper::getInit($params);
require JModuleHelper::getLayoutPath('mod_tmp');

