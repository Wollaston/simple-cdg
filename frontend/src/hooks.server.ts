import type { Handle, HandleFetch } from '@sveltejs/kit';
import { building } from '$app/environment';
import { auth } from '$lib/server/auth';
import { svelteKitHandler } from 'better-auth/svelte-kit';

const handleBetterAuth: Handle = async ({ event, resolve }) => {
    const session = await auth.api.getSession({ headers: event.request.headers });

    if (session) {
        event.locals.session = session.session;
        event.locals.user = session.user;
    }

    return svelteKitHandler({ event, resolve, auth, building });
};

export const handleFetch: HandleFetch = async ({ request, fetch }) => {
    if (request.url.startsWith('http://localhost:3000/')) {
        // clone the original request, but change the URL
        request = new Request(
            request.url.replace('http://localhost:3000/', 'http://sveltekit:3000/'),
            request
        );
    }

    return fetch(request);
};

export const handle: Handle = handleBetterAuth;
