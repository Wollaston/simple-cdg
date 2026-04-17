<script lang="ts">
    import { enhance } from '$app/forms';
    import BillCard from '$lib/components/bills/bill-card.svelte';
    import Button from '$lib/components/ui/button/button.svelte';
    import * as Field from '$lib/components/ui/field/index.js';
    import { Textarea } from '$lib/components/ui/textarea/index.js';
    import type { PageProps } from './$types';

    let { form }: PageProps = $props();
</script>

<div>
    <h1 class="m-2 p-2 pl-4 text-4xl font-bold">Search Bills</h1>
    <div class="m-2 w-full max-w-md p-2">
        <form method="POST" use:enhance>
            <Field.Set>
                <Field.Group>
                    <Field.Field>
                        <Textarea
                            id="query"
                            name="query"
                            placeholder="Search for bills here..."
                            rows={4}
                        />
                    </Field.Field>
                </Field.Group>
            </Field.Set>
            <Field.Field orientation="horizontal" class="m-2 p-2">
                <Button type="submit">Search</Button>
            </Field.Field>
        </form>
    </div>
    {#if form?.bills}
        <div class=" columns-2 gap-4 p-2 md:columns-3">
            {#each form.bills as bill}
                <BillCard text={bill.text} baseId={bill.cdg_id} />
            {/each}
        </div>
    {:else}
        <h1 class="m-2 p-2 text-lg">Retrieved bills will show here...</h1>
    {/if}
</div>
