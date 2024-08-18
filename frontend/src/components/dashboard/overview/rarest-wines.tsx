import * as React from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardHeader from '@mui/material/CardHeader';
import Chip from '@mui/material/Chip';
import Divider from '@mui/material/Divider';
import type { SxProps } from '@mui/material/styles';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import { ArrowRight as ArrowRightIcon } from '@phosphor-icons/react/dist/ssr/ArrowRight';
import dayjs from 'dayjs';

const statusMap = {
  pending: { label: 'Pending', color: 'warning' },
  delivered: { label: 'Delivered', color: 'success' },
  refunded: { label: 'Refunded', color: 'error' },
} as const;

export interface Wine {
  _id: string;
  wine_name: string;
  wine_price: number;
  wine_stock: number;
  wine_category: string;
  status: 'pending' | 'delivered' | 'refunded';
  Date: Date;
}

export interface RarestWinesProps {
  wines?: Wine[];
  sx?: SxProps;
}

export function RarestWines({ wines = [], sx }: RarestWinesProps): React.JSX.Element {
  return (
    <Card sx={sx}>
      <CardHeader title="Rarest Wines" />
      <Divider />
      <Box sx={{ overflowX: 'auto' }}>
        <Table sx={{ minWidth: 800 }}>
          <TableHead>
            <TableRow>
              <TableCell>Wine Name</TableCell>
              <TableCell>Wine Price</TableCell>
              <TableCell>Wine Stock</TableCell>
              <TableCell>Wine Category</TableCell>
              <TableCell sortDirection="desc">Date</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {wines.map((wines) => {
              const { label, color } = statusMap[wines.status] ?? { label: 'Unknown', color: 'default' };

              return (
                <TableRow hover key={wines._id}>
                  <TableCell>{wines.wine_name}</TableCell>
                  <TableCell>{wines.wine_price}</TableCell>
                  <TableCell>{wines.wine_stock}</TableCell>
                  <TableCell>{wines.wine_category}</TableCell>
                  <TableCell>{dayjs(wines.Date).format('MMM D, YYYY')}</TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </Box>
      <Divider />
      <CardActions sx={{ justifyContent: 'flex-end' }}>
        <Button
          color="inherit"
          endIcon={<ArrowRightIcon fontSize="var(--icon-fontSize-md)" />}
          size="small"
          variant="text"
        >
          View all
        </Button>
      </CardActions>
    </Card>
  );
}
