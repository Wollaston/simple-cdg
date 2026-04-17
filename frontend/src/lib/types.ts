interface CdgID {
    congress: string;
    bill_type: string;
    bill_number: string;
}

interface Bill {
    text: string;
    cdg_id: string;
    id: string;
}

interface BillDetail extends Bill {
    congress: number;
    number: number;
    originChamber: string;
    originChamberCode: string;
    title: string;
    type: string;
    raw_text: string;
}

export type { CdgID, Bill, BillDetail };
