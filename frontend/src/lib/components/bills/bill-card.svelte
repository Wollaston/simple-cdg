<script lang="ts">
    import * as Card from '$lib/components/ui/card/index.js';
    import { parseCdgId } from '$lib/utils';
    import type { CdgID } from '$lib/types';
    import Button from '$lib/components/ui/button/button.svelte';

    let { text, baseId }: { text: string; baseId: string } = $props();

    const components: CdgID = parseCdgId(baseId);
</script>

<Card.Root class="m-2 w-full max-w-sm p-2">
    <Card.Header>
        <Card.Title>
            <Button variant="link" href="/bills/detail/{baseId}" class="text-lg">
                {components.bill_type.toUpperCase()}
                {components.bill_number} (Congress {components.congress})
            </Button>
        </Card.Title>
    </Card.Header>
    <Card.Content>
        <p>{text}</p>
    </Card.Content>
</Card.Root>
