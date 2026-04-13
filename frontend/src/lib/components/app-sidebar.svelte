<script lang="ts" module>
    import EllipsisIcon from '@lucide/svelte/icons/ellipsis';
    import FileSearchCorner from '@lucide/svelte/icons/file-search-corner';

    const data = {
        user: {
            name: 'shadcn',
            email: 'm@example.com',
            avatar: '/avatars/shadcn.jpg'
        },
        navMain: [
            {
                title: 'Bills',
                url: '/bills',
                icon: FileSearchCorner,
                isActive: true,
                items: [
                    {
                        title: 'Search',
                        url: '/bills/search'
                    },
                    {
                        title: 'View',
                        url: '/bills/view'
                    },
                    {
                        title: 'Get',
                        url: '/bills/get'
                    }
                ]
            }
        ],
        projects: []
    };
</script>

<script lang="ts">
    import NavMain from './nav-main.svelte';
    import NavProjects from './nav-projects.svelte';
    import NavUser from './nav-user.svelte';
    import * as Sidebar from '$lib/components/ui/sidebar/index.js';
    import CommandIcon from '@lucide/svelte/icons/command';
    import type { ComponentProps } from 'svelte';

    let { ref = $bindable(null), ...restProps }: ComponentProps<typeof Sidebar.Root> = $props();
</script>

<Sidebar.Root bind:ref variant="inset" {...restProps}>
    <Sidebar.Header>
        <Sidebar.Menu>
            <Sidebar.MenuItem>
                <Sidebar.MenuButton size="lg">
                    {#snippet child({ props })}
                        <a href="/" {...props}>
                            <div
                                class="flex aspect-square size-8 items-center justify-center rounded-lg bg-sidebar-primary text-sidebar-primary-foreground"
                            >
                                <CommandIcon class="size-4" />
                            </div>
                            <div class="grid flex-1 text-start text-sm leading-tight">
                                <span class="truncate font-medium">Simple CDG</span>
                                <span class="truncate text-xs">congress.gov Interface</span>
                            </div>
                        </a>
                    {/snippet}
                </Sidebar.MenuButton>
            </Sidebar.MenuItem>
        </Sidebar.Menu>
    </Sidebar.Header>
    <Sidebar.Content>
        <NavMain items={data.navMain} />
        <NavProjects projects={data.projects} />
    </Sidebar.Content>
    <Sidebar.Footer>
        <NavUser user={data.user} />
    </Sidebar.Footer>
</Sidebar.Root>
