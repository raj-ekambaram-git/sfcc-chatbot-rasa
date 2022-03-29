import React from 'react';
import { useSound } from 'use-sound';
import defaultTone from '../../../../../../sounds/default.mp3';

const areEqual = (prevProps, nextProps) => true;

export const MessageTone = React.memo((props) => {
    const [play] = useSound(defaultTone, { volume: 0.5 });
    play();
    return null;
}, areEqual);
