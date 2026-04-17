import { getBills } from '$lib/api/bills.remote';
import type { Actions } from './$types';

export const actions = {
    default: async ({ request }) => {
        const data = await request.formData();
        const query = data.get('query') ?? '';
        const bills = await getBills({ text: query.toString() });

        return { bills };
    }
} satisfies Actions;
