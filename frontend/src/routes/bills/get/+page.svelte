<script lang="ts">
    import { enhance } from '$app/forms';
    import BillsTable from '$lib/components/tables/bills-table.svelte';
    import { Button } from '$lib/components/ui/button/index.js';
    import * as Field from '$lib/components/ui/field/index.js';
    import { Input } from '$lib/components/ui/input/index.js';
    import * as Select from '$lib/components/ui/select/index.js';
    import type { PageProps } from './$types';
    import { columns } from '$lib/components/tables/columns';
    import { Skeleton } from '$lib/components/ui/skeleton';

    let congress = $state<string>('118');
    let bill_type = $state<string>('HR');

    let loading = $state(false);
    const range = Array.from({ length: 119 - 104 + 1 }, (_, i) => i + 104);

    const { form }: PageProps = $props();
</script>

<div class="flex h-screen w-full flex-col px-4">
    <h1 class="m-2 p-2 pl-4 text-4xl font-bold">Get Bills</h1>
    <form
        method="POST"
        use:enhance
        class="w-full"
        use:enhance={() => {
            loading = true;

            return async ({ update }) => {
                loading = false;

                await update();
            };
        }}
    >
        <Field.Group>
            <Field.Set>
                <Field.Description
                    >Use this form to fetch additional bills from the congress.gov API</Field.Description
                >
                <Field.Group>
                    <div class="grid grid-cols-2 gap-4">
                        <Field.Field class="col-span-1">
                            <Field.Label for="congress">Congress</Field.Label>
                            <Select.Root
                                type="single"
                                name="congress"
                                required
                                bind:value={congress}
                            >
                                <Select.Trigger id="checkout-7j9-exp-month-ts6">
                                    <span>
                                        {congress || '118'}
                                    </span>
                                </Select.Trigger>
                                <Select.Content>
                                    {#each range as num}
                                        <Select.Item value={num.toString()}>{num}</Select.Item>
                                    {/each}
                                </Select.Content>
                            </Select.Root>
                            <Field.Description>Session of Congress</Field.Description>
                        </Field.Field>
                        <Field.Field>
                            <Field.Label for="type">Bill Type</Field.Label>
                            <Select.Root type="single" required name="type" bind:value={bill_type}>
                                <Select.Trigger id="checkout-7j9-exp-month-ts6">
                                    <span>
                                        {bill_type || 'HR'}
                                    </span>
                                </Select.Trigger>
                                <Select.Content>
                                    <Select.Item value="HR">HR</Select.Item>
                                    <Select.Item value="S">S</Select.Item>
                                    <Select.Item value="HJRES">HJRES</Select.Item>
                                    <Select.Item value="HCONRES">HCONRES</Select.Item>
                                    <Select.Item value="SRES">SRES</Select.Item>
                                </Select.Content>
                            </Select.Root>
                            <Field.Description>Type of Bill</Field.Description>
                        </Field.Field>
                    </div>
                    <div class="grid grid-cols-2 gap-4">
                        <Field.Field class="col-span-1">
                            <Field.Label for="offset">Offset</Field.Label>
                            <Input id="offset" name="offset" placeholder="8" required />
                            <Field.Description>Offset from First Bill</Field.Description>
                        </Field.Field>
                        <Field.Field class="col-span-1">
                            <Field.Label for="limit">Limit</Field.Label>
                            <Input id="limit" name="limit" placeholder="25" required />
                            <Field.Description>Total Bills to Fetch</Field.Description>
                        </Field.Field>
                    </div>
                </Field.Group>
            </Field.Set>
            <Field.Separator />
            <Field.Field orientation="horizontal">
                <Button type="submit" disabled={loading}>Submit</Button>
            </Field.Field>
        </Field.Group>
    </form>
    {#if form?.bills}
        <BillsTable {columns} data={form.bills} />
    {:else}
        <h1 class="m-2 p-2 text-lg">New bills will show here...</h1>
    {/if}
    {#if loading}
        <div class="flex flex-col space-y-3">
            <Skeleton class="h-8 w-full rounded-xl" />
            <div class="space-y-2">
                <Skeleton class="h-4 w-full" />
                <Skeleton class="h-4 w-full" />
                <Skeleton class="h-4 w-full" />
                <Skeleton class="h-4 w-full" />
            </div>
        </div>
    {/if}
</div>
