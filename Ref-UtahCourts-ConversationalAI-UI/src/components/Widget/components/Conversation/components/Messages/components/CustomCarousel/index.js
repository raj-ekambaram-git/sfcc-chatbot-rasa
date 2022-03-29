import { addUserMessage, emitUserMessage } from 'actions';
import Arrow from 'assets/arrow';
import { PROP_TYPES } from 'constants';
import PropTypes from 'prop-types';
import React, { useContext, useRef, useState } from 'react';
import { connect } from 'react-redux';
import ThemeContext from '../../../../../../ThemeContext';
import './styles.scss';

const CustomCarousel = (props) => {
    const carousel = props.message.toJS();
    const handleClick = (action) => {
        if (!action || action.type !== 'postback') return;
        const { chooseReply } = props;
        chooseReply(action.payload, action.title);
    };

    const scrollContainer = useRef();
    const [leftButton, setLeftButton] = useState(false);
    const [rightButton, setRightButton] = useState(true);
    const { mainColor, assistTextColor } = useContext(ThemeContext);

    const handleScroll = () => {
        const current = scrollContainer.current;
        if (current.scrollLeft > 0) {
            setLeftButton(true);
        } else {
            setLeftButton(false);
        }
        if (current.clientWidth === current.scrollWidth - current.scrollLeft) {
            setRightButton(false);
        } else {
            setRightButton(true);
        }
    };

    const handleLeftArrow = () => {
        scrollContainer.current.scrollTo({
            left: scrollContainer.current.scrollLeft - 230,
            behavior: 'smooth',
        });
    };

    const handleRightArrow = () => {
        scrollContainer.current.scrollTo({
            left: scrollContainer.current.scrollLeft + 230,
            behavior: 'smooth',
        });
    };

    const toPascalCase = (string) => {
        return string.replace(/\w+/g, function (w) {
            return w[0].toUpperCase() + w.slice(1).toLowerCase();
        });
    };

    const populateCard = (cardObj) => {
        let elements = [];
        for (var key in cardObj) {
            if (cardObj.hasOwnProperty(key)) {
                var value = cardObj[key];
                elements.push(
                    <div className="rw-carousel-card-subtitle" key={key}>
                        {toPascalCase(key)}
                    </div>
                );
                elements.push(
                    <div className="rw-carousel-card-title" key={key + value}>
                        {value}
                    </div>
                );
            }
        }
        return elements;
    };

    const { linkTarget } = props;

    return (
        <React.Fragment>
            <div
                className="rw-carousel-container"
                ref={scrollContainer}
                onScroll={() => handleScroll()}
            >
                {carousel.elements.map((element, index) => {
                    return (
                        <div className="rw-carousel-card" key={index}>
                            <div className="rw-carousel-card-subtitle">{carousel.title}</div>
                            <div className="rw-hr-line"> </div>
                            {populateCard(element)}
                        </div>
                    );
                })}
            </div>
            {carousel.elements.length > 1 && (
                <div className="rw-carousel-arrows-container">
                    {leftButton && (
                        // eslint-disable-next-line jsx-a11y/no-static-element-interactions
                        <div
                            className="rw-left-arrow rw-carousel-arrow"
                            onClick={handleLeftArrow}
                            role="button"
                            tabIndex={0}
                        >
                            <div className="rw-arrow" alt="left carousel arrow">
                                <Arrow />
                            </div>
                        </div>
                    )}
                    {rightButton && (
                        // eslint-disable-next-line jsx-a11y/no-static-element-interactions
                        <div
                            className="rw-right-arrow rw-carousel-arrow"
                            onClick={handleRightArrow}
                            role="button"
                            tabIndex={0}
                        >
                            <div className="rw-arrow" alt="right carousel arrow">
                                <Arrow />
                            </div>
                        </div>
                    )}
                </div>
            )}
        </React.Fragment>
    );
};

CustomCarousel.propTypes = {
    message: PROP_TYPES.CUSTOM_CAROUSEL,
    // completely bugged, it's actually used in handle click
    // eslint-disable-next-line react/no-unused-prop-types
    chooseReply: PropTypes.func.isRequired,
    linkTarget: PropTypes.string,
};

const mapStateToProps = (state) => ({
    linkTarget: state.metadata.get('linkTarget'),
});

const mapDispatchToProps = (dispatch) => ({
    chooseReply: (payload, title) => {
        if (title) dispatch(addUserMessage(title));
        dispatch(emitUserMessage(payload));
    },
});

export default connect(mapStateToProps, mapDispatchToProps)(CustomCarousel);
