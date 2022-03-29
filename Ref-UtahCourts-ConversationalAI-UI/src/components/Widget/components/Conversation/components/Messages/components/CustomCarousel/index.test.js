import { shallow } from 'enzyme';
import { createCustomCarousel } from 'helper';
import { List } from 'immutable';
import React from 'react';
import { Provider } from 'react-redux';
import LocalStorageMock from '../../../../../../../../../mocks/localStorageMock';
import { initStore } from '../../../../../../../../store/store';
import Messages from '../../index';

describe('</CustomCarousel />', () => {
    const carousel = createCustomCarousel(
        {
            attachment: {
                type: 'template',
                payload: {
                    template_type: 'generic',
                    name: 'custom_carousel',
                    title: 'Case Offense Details',
                    elements: [
                        {
                            sequence: '1',
                            offense: '53-3-202(1)(A) - NO VALID LICENSE - EXPIRED',
                            severity: 'Infraction',
                            offense_date: '07/25/2019',
                        },
                        {
                            sequence: '2',
                            offense: '53-3-202(1)(A) - NO VALID LICENSE - EXPIRED',
                            severity: 'Infraction',
                            offense_date: '07/25/2019',
                        },
                        {
                            sequence: '3',
                            offense: '53-3-202(1)(A) - NO VALID LICENSE - EXPIRED',
                            severity: 'Infraction',
                            offense_date: '07/25/2019',
                        },
                    ],
                },
            },
            text: 'undefined',
        },
        'response'
    );

    const responseMessage = List([carousel]);

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
        expect(messagesComponent.render().find('.rw-carousel-card')).toHaveLength(3);
        expect(messagesComponent.render().find('a[href^="https://google"]')).toHaveLength(3);
        expect(messagesComponent.render().find('.rw-reply')).toHaveLength(3);

        expect(messagesComponent.render().find('.rw-reply[href^="https://facebook"]')).toHaveLength(
            1
        );
    });
});
