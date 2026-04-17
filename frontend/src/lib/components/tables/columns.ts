import type { ColumnDef } from '@tanstack/table-core';
import type { BillDetail } from '$lib/types';
import { createRawSnippet } from 'svelte';
import { renderComponent, renderSnippet } from '../ui/data-table';
import NumberButton from './number-button.svelte';

export const columns: ColumnDef<BillDetail>[] = [
    {
        accessorKey: 'title',
        header: 'Title',
        cell: ({ row }) => {
            const cdgIdCellSnippet = createRawSnippet<[{ title: string }]>((getTitle) => {
                return {
                    render: () => `<div class="max-w-sm truncate">${getTitle().title}</div>`
                };
            });

            return renderSnippet(cdgIdCellSnippet, {
                title: row.original.title
            });
        }
    },
    {
        accessorKey: 'originChamber',
        header: 'Chamber'
    },
    {
        accessorKey: 'number',
        header: ({ column }) =>
            renderComponent(NumberButton, {
                onclick: column.getToggleSortingHandler()
            }),
        cell: ({ row }) => {
            const billnumberCellSnippet = createRawSnippet<[{ number: number }]>(
                (getBillNumber) => {
                    return {
                        render: () => `<div>${getBillNumber().number}</div>`
                    };
                }
            );

            return renderSnippet(billnumberCellSnippet, {
                number: row.original.number
            });
        }
    },
    {
        accessorKey: 'type',
        header: 'Type'
    },
    {
        accessorKey: 'congress',
        header: 'Congress'
    },
    {
        accessorKey: 'cdg_id',
        header: 'Detail',
        cell: ({ row }) => {
            const cdgIdCellSnippet = createRawSnippet<[{ cdg_id: string }]>((getId) => {
                const { cdg_id } = getId();
                return {
                    render: () =>
                        `<div class="font-medium text-blue-500 hover:underline"><a href="/bills/detail/${cdg_id}">Detail</a></div>`
                };
            });

            return renderSnippet(cdgIdCellSnippet, {
                cdg_id: row.original.cdg_id
            });
        }
    }
];
