import { addUserMessage, emitUserMessage } from 'actions';
import { PROP_TYPES } from 'constants';
import PropTypes from 'prop-types';
import React, { useRef } from 'react';
import { connect } from 'react-redux';
import './styles.scss';

const CustomCard = (props) => {
    const customCard = props.message.toJS();

    const scrollContainer = useRef();

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

    const { linkTarget } = props;

    return (
        <React.Fragment>
            <div
                className="rw-custom-container"
                ref={scrollContainer}
                onScroll={() => handleScroll()}
            >
                <div className="rw-custom-card">
                    <div className="rw-custom-card-title">{customCard.title}</div>
                    <div className="rw-hr-line"> </div>
                    <div className="rw-custom-card-text">{customCard.text}</div>
                    <form
                        name={customCard.form.name}
                        id={customCard.form.id}
                        action={customCard.form.action}
                        method={customCard.form.method}
                        target={customCard.form.target}
                    >
                        {customCard.form.elements.map((element, index) => {
                            return (
                                <input
                                    key={index}
                                    type="hidden"
                                    name={element.name}
                                    value={element.value}
                                />
                            );
                        })}
                        <div
                            className="rw-custom-card-button"
                            onClick={() =>
                                document.getElementById(`${customCard.form.id}`).submit()
                            }
                        >
                            {customCard.form.link_title}
                        </div>
                    </form>
                </div>
            </div>
        </React.Fragment>
    );
};

CustomCard.propTypes = {
    message: PROP_TYPES.CUSTOM_CARD,
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

export default connect(mapStateToProps, mapDispatchToProps)(CustomCard);
