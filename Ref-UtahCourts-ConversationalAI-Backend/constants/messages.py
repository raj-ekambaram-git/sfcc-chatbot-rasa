CASE_BUTTON_TITLE = '🔖 {case_number} - {case_title}'
CASE_DETAILS_BUTTON_PAYLOAD = '/provide_case_details{{"case_number" : "{case_number}", "court_type" : "{court_type}", "location_code" : "{location_code}"}}'
CASE_CUSTOM_JSON = {
    'attachment': {
        'type': 'template',
        'payload': {
            'template_type': 'generic',
            'name': 'custom_carousel',
            'title': 'Case Details',
            'elements': []
        }
    }
}
CASE_CHARGE_CUSTOM_JSON = {
    'attachment': {
        'type': 'template',
        'payload': {
            'template_type': 'generic',
            'name': 'custom_carousel',
            'title': 'Case Offense Details',
            'elements': []
        }
    }
}

CASE_PARTY_CUSTOM_JSON = {
    'attachment': {
        'type': 'template',
        'payload': {
            'template_type': 'generic',
            'name': 'custom_carousel',
            'title': 'Case Party Details',
            'elements': []
        }
    }
}

CASE_HEARING_DATE_CUSTOM_JSON = {
    'attachment': {
        'type': 'template',
        'payload': {
            'template_type': 'generic',
            'name': 'custom_carousel',
            'title': 'Case Hearing Details',
            'elements': []
        }
    }
}

CASE_PAYMENT_CUSTOM_JSON = {
    'attachment': {
        'type': 'template',
        'payload': {
            'template_type': 'generic',
            'name': 'payment_form',
            'title': 'Payment',
            'isForm': True,
            'text': 'You owe ${epay_amount}. To pay the amount owed for your case {case_number}, please click the button below',
            'form': {
                'name': 'chatbotEpaymentDetail',
                'id': 'chatbotEpaymentDetailId_{timestamp}',
                'action': '',
                'method': 'post',
                'target': '_blank',
                'link_title': 'Make a payment',
                'elements': []},
        }}}
