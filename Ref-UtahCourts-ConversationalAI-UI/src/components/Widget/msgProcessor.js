export function isCarousel(message) {
    return (
        Object.keys(message).includes('attachment') &&
        Object.keys(message.attachment).includes('type') &&
        message.attachment.type === 'template' &&
        Object.keys(message.attachment).includes('payload') &&
        Object.keys(message.attachment.payload).indexOf('template_type') >= 0 &&
        message.attachment.payload.template_type === 'generic' &&
        Object.keys(message.attachment.payload).indexOf('elements') >= 0 &&
        message.attachment.payload.elements.length > 0
    );
}

export function isCustomCarousel(message) {
    return (
        Object.keys(message).includes('attachment') &&
        Object.keys(message.attachment).includes('type') &&
        message.attachment.type === 'template' &&
        Object.keys(message.attachment).includes('payload') &&
        Object.keys(message.attachment.payload).indexOf('template_type') >= 0 &&
        message.attachment.payload.template_type === 'generic' &&
        message.attachment.payload.name === 'custom_carousel' &&
        Object.keys(message.attachment.payload).indexOf('elements') >= 0 &&
        message.attachment.payload.elements.length > 0
    );
}

export function isCustomCard(message) {
    return (
        Object.keys(message).includes('attachment') &&
        Object.keys(message.attachment).includes('type') &&
        message.attachment.type === 'template' &&
        Object.keys(message.attachment).includes('payload') &&
        Object.keys(message.attachment.payload).indexOf('template_type') >= 0 &&
        message.attachment.payload.template_type === 'generic' &&
        message.attachment.payload.name === 'payment_form' &&
        message.attachment.payload.isForm &&
        Object.keys(message.attachment.payload.form).indexOf('elements') >= 0 &&
        message.attachment.payload.form.elements.length > 0
    );
}

export function isVideo(message) {
    return (
        Object.keys(message).includes('attachment') &&
        Object.keys(message.attachment).includes('type') &&
        message.attachment.type === 'video'
    );
}

export function isImage(message) {
    return (
        Object.keys(message).includes('attachment') &&
        Object.keys(message.attachment).includes('type') &&
        message.attachment.type === 'image'
    );
}

export function isText(message) {
    return Object.keys(message).includes('text');
}

export function isButtons(message) {
    return (
        Object.keys(message).includes('text') &&
        (Object.keys(message).includes('quick_replies') || Object.keys(message).includes('buttons'))
    );
}
