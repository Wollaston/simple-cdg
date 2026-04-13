import { query } from '$app/server';
import * as v from 'valibot';

const BillsSchema = v.object({
    text: v.string(),
    begin: v.number(),
    end: v.number()
});

export const getBills = query(BillsSchema, async (input) => {
    const res = await fetch(`http://localhost:8000/bills/search/10`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json'
        },
        body: JSON.stringify({ text: input.text })
    });
    const bills = await res.json();

    return bills;
});
