<script lang="ts">
    import * as Card from '$lib/components/ui/card/index.js';

    let { id, text }: { id: string; text: string } = $props();
</script>

<Card.Root class="m-2 w-full max-w-sm p-2">
    <Card.Header>
        <Card.Title>Bill</Card.Title>
        <Card.Description>ID: {id}</Card.Description>
    </Card.Header>
    <Card.Content>
        <p>{text}</p>
    </Card.Content>
</Card.Root>
