more_info_whitelist = '-c tessedit_char_whitelist=MoreInfo'
number_whitelist = '-c tessedit_char_whitelist=0123456789'
psm_number_whitelist = '--psm 6 -c tessedit_char_whitelist=0123456789'

ROKSCAN_DATA = {
    'more_info_check': {
        'roi': (294, 786, 116, 29),
        'character_white_list': more_info_whitelist,
        'is_darkfont': True,
        'has_blur': False,
    },
    'gov_id_image': {
        'roi': (733, 192, 200, 35),
        'character_white_list': number_whitelist,
        'is_darkfont': False,
        'has_blur': False,
    },
    'gov_killpoints_image': {
        'roi': (1106, 327, 224, 40),
        'character_white_list': number_whitelist,
        'is_darkfont': False,
        'has_blur': False,
    },
    'gov_kills_high_image': {
        'roi': (1000, 400, 165, 50),
        'character_white_list': psm_number_whitelist,
        'is_darkfont': True,
        'has_blur': False,
    },
    'gov_power_image': {
        'roi': (874, 327, 224, 40),
        'character_white_list': psm_number_whitelist,
        'is_darkfont': False,
        'has_blur': False,
    },
    'alliance_tag_image': {
        'roi': (598, 331, 250, 40),
        'character_white_list': '',
        'is_darkfont': True,
        'has_blur': False,
    },
    'gov_deads_high_image': {
        'roi': (1000, 480 , 199, 35),
        'character_white_list': number_whitelist,
        'is_darkfont': True,
        'has_blur': False,
    },
    'gov_sevs_high_image': {
        'roi': (1000, 530 , 199, 35),
        'character_white_list': number_whitelist,
        'is_darkfont': True,
        'has_blur': False,
    },
    'kills_tiers_image': {
        'roi': (862, 'y', 215, 26),
        'character_white_list': psm_number_whitelist,
        'is_darkfont': True,
        'has_blur': False,
    },
    'kills_tiers_image': {
        'roi': (862, 'y', 215, 26),
        'character_white_list': psm_number_whitelist,
        'is_darkfont': True,
        'has_blur': False,
    },
    'gov_dead_image': {
        'roi': (1130, 443, 183, 40),
        'character_white_list': psm_number_whitelist,
        'is_darkfont': True,
        'has_blur': True,
    },
    'gov_rss_assistance_image': {
        'roi': (1130, 668, 183, 40),
        'character_white_list': psm_number_whitelist,
        'is_darkfont': True,
        'has_blur': True,
    },
    'gov_helps_image': {
        'roi': (1148, 732, 164, 44),
        'character_white_list': psm_number_whitelist,
        'is_darkfont': True,
        'has_blur': True,
    },
}