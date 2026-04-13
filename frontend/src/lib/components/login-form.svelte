<script lang="ts">
    import { Button } from '$lib/components/ui/button/index.js';
    import * as Card from '$lib/components/ui/card/index.js';
    import { Input } from '$lib/components/ui/input/index.js';
    import {
        FieldGroup,
        Field,
        FieldLabel,
        FieldDescription
    } from '$lib/components/ui/field/index.js';
    import { enhance } from '$app/forms';
    import type { ActionData } from '../../routes/auth/login/$types';

    let { form }: { form: ActionData } = $props();
    const id = $props.id();
</script>

<Card.Root class="mx-auto w-full max-w-sm">
    <Card.Header>
        <Card.Title class="text-2xl">Login</Card.Title>
        <Card.Description
            >Enter your email and password below to login to your account</Card.Description
        >
    </Card.Header>
    <Card.Content>
        <form method="post" action="?/signInEmail" use:enhance>
            <FieldGroup>
                <Field>
                    <FieldLabel for="email-{id}">Email</FieldLabel>
                    <Input
                        id="email-{id}"
                        type="email"
                        name="email"
                        placeholder="me@example.com"
                        required
                    />
                </Field>
                <Field>
                    <div class="flex items-center">
                        <FieldLabel for="password-{id}">Password</FieldLabel>
                        <a href="##" class="ms-auto inline-block text-sm underline">
                            Forgot your password?
                        </a>
                    </div>
                    <Input id="password-{id}" name="password" type="password" required />
                </Field>
                <Field>
                    <p class="text-red-500">{form?.message ?? ''}</p>
                    <Button type="submit" class="w-full">Login</Button>
                    <FieldDescription class="text-center">
                        Don't have an account? <a href="/auth/register">Sign up</a>
                    </FieldDescription>
                </Field>
            </FieldGroup>
        </form>
    </Card.Content>
</Card.Root>
