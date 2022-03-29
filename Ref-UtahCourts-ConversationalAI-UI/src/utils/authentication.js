import { post } from './fetch';

function authenticate(customData) {
    if ('token' in customData) {
        return new Promise((resolve, reject) => {
            post(customData.authUrl, {
                token: customData.token,
                dev: true,
            })
                .then((response) => {
                    sessionStorage.setItem('ACCESS_TOKEN', response.accessToken);
                    resolve();
                })
                .catch((error) => {
                    if (sessionStorage.getItem('ACCESS_TOKEN'))
                        sessionStorage.removeItem('ACCESS_TOKEN');
                    reject();
                });
        });
    } else {
        return new Promise((resolve, reject) => {
            window.getChatbotAuthenticationToken((data) => {
                if (!data.error) {
                    post(customData.authUrl, {
                        token: data.results,
                    })
                        .then((response) => {
                            sessionStorage.setItem('ACCESS_TOKEN', response.accessToken);
                            resolve();
                        })
                        .catch((error) => {
                            if (sessionStorage.getItem('ACCESS_TOKEN'))
                                sessionStorage.removeItem('ACCESS_TOKEN');
                            reject();
                        });
                } else {
                    if (sessionStorage.getItem('ACCESS_TOKEN'))
                        sessionStorage.removeItem('ACCESS_TOKEN');
                    reject();
                }
            });
        });
    }
}
export { authenticate };
