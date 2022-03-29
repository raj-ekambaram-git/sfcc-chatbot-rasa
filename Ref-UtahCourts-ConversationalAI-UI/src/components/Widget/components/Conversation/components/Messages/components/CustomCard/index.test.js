import { shallow } from 'enzyme';
import { createCustomCard } from 'helper';
import { List } from 'immutable';
import React from 'react';
import { Provider } from 'react-redux';
import LocalStorageMock from '../../../../../../../../../mocks/localStorageMock';
import { initStore } from '../../../../../../../../store/store';
import Messages from '../../index';

describe('</CustomCard />', () => {
    const card = createCustomCard(
        {
            attachment: {
                type: 'template',
                payload: {
                    template_type: 'generic',
                    name: 'payment_form',
                    title: 'Payment',
                    text: 'To pay the amount owed for your case 123456789, please click the link below',
                    action: '',
                    method: '',
                    target: '',
                    elements: [
                        {
                            name: '',
                            value: '',
                        },
                        {
                            name: '',
                            value: '',
                        },
                        {
                            name: '',
                            value: '',
                        },
                    ],
                },
            },
            text: 'undefined',
        },
        'response'
    );

    const responseMessage = List([card]);

    const localStorage = new LocalStorageMock();

    const store = initStore('dummy', 'dummy', localStorage);

    store.dispatch({
        type: 'CONNECT',
    });

    const messagesComponent = shallow(
        <Provider store={store}>
            <Messages.WrappedComponent messages={responseMessage} />
        </Provider>
    );

    it('should render a Carousel component and buttons and default actions', () => {
        expect(messagesComponent.render().find('.rw-card-card')).toHaveLength(3);
        expect(messagesComponent.render().find('a[href^="https://google"]')).toHaveLength(3);
        expect(messagesComponent.render().find('.rw-reply')).toHaveLength(3);

        expect(messagesComponent.render().find('.rw-reply[href^="https://facebook"]')).toHaveLength(
            1
        );
    });
});
