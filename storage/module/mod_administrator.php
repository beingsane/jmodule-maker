<?php

/* 
 * MODULE: mod_administrator
 * AUTHOR: IT Services
 * VERSION: 1.0
 * 
 * Unauthorized copying of this file, via any medium is strictly prohibited
 * Proprietary and confidential
 * Copyright (c) 2017, SM Retail, Inc.
 * All rights reserved.
 */


// No direct access
defined('_JEXEC') or die;
// Include the syndicate function only once
require_once dirname(__FILE__) . '/helper.php';

$z = ModAdministratorHelper::getInit($params);
require JModuleHelper::getLayoutPath('mod_administrator');

