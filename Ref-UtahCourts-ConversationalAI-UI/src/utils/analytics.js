function getDeviceType() {
    const userAgent = navigator.userAgent;
    if (/(tablet|ipad|playbook|silk)|(android(?!.*mobi))/i.test(userAgent)) {
        return 'Tablet';
    }
    if (
        /Mobile|iP(hone|od)|Android|BlackBerry|IEMobile|Kindle|Silk-Accelerated|(hpw|web)OS|Opera M(obi|ini)/.test(
            userAgent
        )
    ) {
        return 'Mobile';
    }
    return 'Desktop';
}

function isIOS() {
    return (
        ['iPad Simulator', 'iPhone Simulator', 'iPod Simulator', 'iPad', 'iPhone', 'iPod'].includes(
            navigator.platform
        ) ||
        (navigator.userAgent.includes('Mac') && 'ontouchend' in document)
    );
}

function getBrowser() {
    const { userAgent } = navigator;
    let match =
        userAgent.match(/(opera|chrome|safari|firefox|msie|trident(?=\/))\/?\s*(\d+)/i) || [];
    let temp;

    if (/trident/i.test(match[1])) {
        temp = /\brv[ :]+(\d+)/g.exec(userAgent) || [];

        return `IE ${temp[1] || ''}`;
    }

    if (match[1] === 'Chrome') {
        temp = userAgent.match(/\b(OPR|Edge)\/(\d+)/);

        if (temp !== null) {
            return temp.slice(1).join(' ').replace('OPR', 'Opera');
        }

        temp = userAgent.match(/\b(Edg)\/(\d+)/);

        if (temp !== null) {
            return temp.slice(1).join(' ').replace('Edg', 'Edge (Chromium)');
        }
    }

    match = match[2] ? [match[1], match[2]] : [navigator.appName, navigator.appVersion, '-?'];
    temp = userAgent.match(/version\/(\d+)/i);

    if (temp !== null) {
        match.splice(1, 1, temp[1]);
    }

    return match.join(' ');
}

function getTimeZone() {
    return Intl.DateTimeFormat().resolvedOptions().timeZone;
}

function getAnalyticsData() {
    return {
        deviceType: getDeviceType(),
        browser: getBrowser(),
        timeZone: getTimeZone(),
        timestamp: new Date().toISOString(),
    };
}

export { getAnalyticsData, getDeviceType, isIOS };
