import { newBills } from '$lib/api/new-bills.remote';
import type { Actions } from './$types';

export const actions = {
    default: async ({ request }) => {
        const data = await request.formData();
        const congress = data.get('congress') ?? '118';
        const type = data.get('type') ?? 'hr';
        const offset = data.get('offset') ?? '0';
        const limit = data.get('limit') ?? '10';
        const bills = await newBills({
            congress: congress.toString(),
            type: type.toString(),
            offset: offset.toString(),
            limit: limit.toString()
        });

        return { bills };
    }
} satisfies Actions;
