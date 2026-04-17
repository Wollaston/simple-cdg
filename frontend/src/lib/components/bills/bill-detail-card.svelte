<script lang="ts">
    import * as Card from '$lib/components/ui/card/index.js';
    import type { BillDetail } from '$lib/types';

    let { congress, number, originChamber, title, type, raw_text }: BillDetail = $props();
</script>

<Card.Root class="-my-4 w-full max-w-xl">
    <Card.Header>
        <Card.Title>{title}</Card.Title>
        <Card.Description>{type} {number} (Congress {congress}) in {originChamber}</Card.Description
        >
    </Card.Header>
    <Card.Content>
        <div>{@html raw_text}</div>
    </Card.Content>
</Card.Root>
