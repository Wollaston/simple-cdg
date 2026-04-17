import { query } from '$app/server';
import { BACKEND_HOST, BACKEND_PORT } from '$env/static/private';
import type { Bill } from '$lib/types';
import * as v from 'valibot';

const BillsSchema = v.object({
    text: v.string()
});

export const getBills = query(BillsSchema, async (input): Promise<Bill[]> => {
    const res = await fetch(`http://${BACKEND_HOST}:${BACKEND_PORT}/bills/search/10`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json'
        },
        body: JSON.stringify({ text: input.text })
    });
    const bills: Promise<Bill[]> = await res.json();

    return bills;
});
